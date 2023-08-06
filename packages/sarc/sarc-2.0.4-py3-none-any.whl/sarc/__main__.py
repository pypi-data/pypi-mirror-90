# Copyright 2018 leoetlino <leo@leolam.fr>
# Licensed under GPLv2+

import argparse
import io
import os
import shutil
import struct
import sys
import typing

from . import sarc
import oead

def sarc_extract(args) -> None:
    target_dir: typing.Optional[str] = args.directory
    with open(args.sarc, "rb") as f:
        s = sarc.read_file_and_make_sarc(f)
        if not s:
            sys.stderr.write("Unknown file format\n")
            sys.exit(1)
        if target_dir:
            s.extract_to_dir(target_dir, print_names=True)
        else:
            s.extract(args.sarc, print_names=True)

def sarc_list(args) -> None:
    with open(args.sarc, "rb") as f:
        s = sarc.read_file_and_make_sarc(f)
        if not s:
            sys.stderr.write("Unknown file format\n")
            sys.exit(1)
        for file in sorted(s.list_files()):
            extra_info = "[0x%x bytes]" % s.get_file_size(file)
            extra_info += " @ 0x%x" % s.get_file_data_offset(file)
            print("%s%s" % (file, ' ' + extra_info if not args.name_only else ''))

def _write_sarc(writer: sarc.SARCWriter, dest_file: str, dest_stream: typing.BinaryIO) -> None:
    buf = io.BytesIO()
    alignment: int = writer.write(buf)
    buf.seek(0)

    extension = os.path.splitext(dest_file)[1]
    if extension.startswith('.s') and extension != '.sarc':
        # sead::ParallelSZSDecompressor::tryDecompFromDevice allocates the read buffer
        # with arg->alignment or max(yaz0_header->alignment, 0x20) if no specific alignment
        # was requested by the calling code.
        # So we need to make sure that the alignment value is kept.
        dest_stream.write(oead.yaz0.compress(buf.getbuffer(), data_alignment=(alignment if alignment > 0x20 else 0)))
    else:
        shutil.copyfileobj(buf, dest_stream)

def sarc_create_or_update(args, update: bool) -> None:
    file_list: typing.List[str] = args.files
    dest_file: str = args.dest
    base_path: typing.Optional[str] = args.base_path

    if '!!' in dest_file:
        if len(file_list) != 1:
            sys.stderr.write('error: cannot detect what the output SARC name should be from file list\n')
            sys.exit(1)
        dest_file = dest_file.replace('!!', os.path.normpath(file_list[0]))

    if not args.base_path:
        if len(file_list) != 1:
            sys.stderr.write('error: cannot auto detect base path from file list\n')
            sys.exit(1)
        if not os.path.isdir(file_list[0]) and os.path.isdir(dest_file):
            sys.stderr.write(f'error: {file_list[0]} is not a directory. Did you mix up the argument order? (directory that should be archived first, then the target SARC)\n')
            sys.exit(1)
        if os.path.isdir(file_list[0]):
            base_path = file_list[0]
        else:
            base_path = os.getcwd()

    writer: typing.Optional[sarc.SARCWriter] = None
    if not update:
        writer = sarc.SARCWriter(be=args.be)
    else:
        with open(dest_file, 'rb') as original_sarc_file:
            writer = sarc.read_sarc_and_make_writer(original_sarc_file, None)

    if not writer:
        sys.stderr.write('error: could not create SARC writer (is the original SARC valid?)\n')
        sys.exit(1)

    writer.set_align_for_nested_sarc(args.align_nested_sarc)
    if update and args.endian:
        writer.set_big_endian(args.endian == 'be')
    if not update and args.default_alignment:
        writer.set_default_alignment(args.default_alignment)

    dest_stream: typing.BinaryIO = open(dest_file, 'wb') if dest_file != '-' else sys.stdout.buffer

    def add_file(writer: sarc.SARCWriter, path: str) -> None:
        with open(path, 'rb') as f:
            archive_path = path if not base_path else os.path.relpath(path=path, start=base_path)
            archive_path = archive_path.replace('\\', '/')
            if args.with_leading_slash and archive_path[0] != '/':
                archive_path = '/' + archive_path
            writer.add_file(archive_path, f.read())
            sys.stderr.write(archive_path + '\n')

    for file in file_list:
        if os.path.isfile(file):
            add_file(writer, file)
        else:
            for root, dirs, files in os.walk(file, topdown=False):
                for file_name in files:
                    add_file(writer, os.path.join(root, file_name))

    _write_sarc(writer, dest_file, dest_stream)

def sarc_delete(args) -> None:
    files_to_remove: typing.List[str] = args.files
    dest_file: str = args.archive

    def should_keep_file(entry: str) -> bool:
        for file_to_remove in files_to_remove:
            if file_to_remove.endswith('/') and entry.startswith(file_to_remove): # directory
                return False
            if entry == file_to_remove:
                return False
        return True

    writer: typing.Optional[sarc.SARCWriter] = None
    with open(dest_file, 'rb') as original_sarc_file:
        writer = sarc.read_sarc_and_make_writer(original_sarc_file, should_keep_file)

    if not writer:
        sys.stderr.write('error: could not create SARC writer (is the original SARC valid?)\n')
        sys.exit(1)

    dest_stream: typing.BinaryIO = open(dest_file, 'wb') if dest_file != '-' else sys.stdout.buffer
    writer.set_align_for_nested_sarc(args.align_nested_sarc)
    _write_sarc(writer, dest_file, dest_stream)

def sarc_test_repack(args) -> None:
    archive = sarc.read_file_and_make_sarc(args.archive)
    if not archive:
        sys.exit(10)

    writer = sarc.make_writer_from_sarc(archive, None)
    if not writer:
        sys.exit(11)
    writer.set_align_for_nested_sarc(args.align_nested_sarc)

    original_offsets = archive.get_file_offsets()
    repacked_offsets = writer.get_file_offsets()

    for original_offset, repacked_offset in zip(original_offsets, repacked_offsets):
        if original_offset == repacked_offset:
            print('%s @ 0x%x' % (original_offset[0], original_offset[1]))
        else:
            print('')
            print('!!! mismatch: original: %s @ 0x%x' % (original_offset[0], original_offset[1]))
            print('!!! mismatch: repacked: %s @ 0x%x' % (repacked_offset[0], repacked_offset[1]))
            if original_offset[1] > repacked_offset[1]:
                alignment = 2
                aligned_offset = repacked_offset[1]
                while aligned_offset != original_offset[1]:
                    alignment <<= 1
                    aligned_offset = (aligned_offset + alignment - 1) & -alignment
                print('!!! mismatch: alignment value seems to be 0x%x' % alignment)
            sys.exit(12)

    buf = io.BytesIO()
    writer.write(buf)
    if archive._data != buf.getbuffer():
        print('!!! mismatch: repacked archive is different')
        sys.exit(13)

    print('ok')

def main() -> None:
    parser = argparse.ArgumentParser(description='Tool to extract or list files in a SARC archive.')

    subparsers = parser.add_subparsers(dest='command', help='Command')
    subparsers.required = True

    x_parser = subparsers.add_parser('extract', description='Extract an archive', aliases=['x'])
    x_parser.add_argument('sarc', help='Path to an SARC archive')
    x_parser.add_argument('--directory', '-C', help='Target directory')
    x_parser.set_defaults(func=sarc_extract)

    l_parser = subparsers.add_parser('list', description='List files in an archive', aliases=['l'])
    l_parser.add_argument('sarc', help='Path to an SARC archive')
    l_parser.add_argument('--name-only', action='store_true', help='Show only file names')
    l_parser.set_defaults(func=sarc_list)

    c_parser = subparsers.add_parser('create', description='Create an archive', aliases=['c'])
    c_parser.add_argument('-b', '--be', action='store_true', help='Use big endian. Defaults to false.')
    c_parser.add_argument('--base-path', help='Base path to remove from contained file names.')
    c_parser.add_argument('--with-leading-slash', action='store_true', help='Add a leading slash to all paths. Required for some game data archives.')
    c_parser.add_argument('-n', '--default-alignment', type=lambda n: int(n, 0),
                          help='Set the default alignment for files. Defaults to 4.')
    c_parser.add_argument('files', nargs='+', help='Files or directories to include in the archive')
    c_parser.add_argument('dest', help='Destination archive')
    c_parser.set_defaults(func=lambda a: sarc_create_or_update(a, update=False))

    u_parser = subparsers.add_parser('update', description='Update an archive', aliases=['u'])
    u_parser.add_argument('--base-path', help='Base path to remove from contained file names.')
    u_parser.add_argument('--with-leading-slash', action='store_true', help='Add a leading slash to all paths. Required for some game data archives.')
    u_parser.add_argument('--endian', choices=['le', 'be'], help='Override endianness. By default sarctool keeps the endianness of the original archive.')
    u_parser.add_argument('files', nargs='+', help='Files or directories to add to the archive')
    u_parser.add_argument('dest', help='Archive to update')
    u_parser.set_defaults(func=lambda a: sarc_create_or_update(a, update=True))

    d_parser = subparsers.add_parser('delete', description='Delete files from an archive', aliases=['d'])
    d_parser.add_argument('files', nargs='+', help='Files or directories to remove from the archive (paths are relative to archive)')
    d_parser.add_argument('archive', help='Archive to update')
    d_parser.set_defaults(func=sarc_delete)

    t_parser = subparsers.add_parser('test-repack', description='Test repacking to check for potential alignment issues')
    t_parser.add_argument('archive', type=argparse.FileType('rb'), help='Archive to test')
    t_parser.set_defaults(func=sarc_test_repack)

    for p in [c_parser, u_parser, d_parser, t_parser]:
        p.add_argument('-A', '--align-nested-sarc', '--not-botw', action='store_true', help='Align nested SARCs to 0x2000 byte boundaries and do *not* assume the game resource system will handle alignment. Useless and even harmful for BotW, but required for some games. Defaults to false.')

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
