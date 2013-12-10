from util import *

# Before build, download proprietary drivers from https://developers.google.com/android/nexus/drivers,
# and put them into related directory under /workspace/topic/android/backup/vendor.
# jdk must be 1.6.0.45 for 4.4 build, and JAVA_HOME should be set correctly.

# build time: 4.4 - 1 hour

root_dir = '/workspace/project/android/'
backup_dir = '/workspace/topic/android/backup/'
backup_driver_dir = backup_dir + 'vendor/'
backup_image_dir = backup_dir + 'image/'
device = ''
device_code_name = ''
variant = ''
version = ''

def handle_option():
    global args

    parser = argparse.ArgumentParser(description = 'Script to sync, build Android',
                                     formatter_class = argparse.RawTextHelpFormatter,
                                     epilog = '''
examples:

  python %(prog)s -s android-4.4_r1.2
  python %(prog)s -f all

  python %(prog)s -s android-4.3_r1 -b -f all

''')

    parser.add_argument('-s', '--sync', dest='sync', help='tag to sync')
    parser.add_argument('-b', '--build', dest='build', help='build', action='store_true')
    parser.add_argument('-f', '--flash', dest='flash', help='type to flash', choices=['all'])

    parser.add_argument('-d', '--device', dest='device', help='device', choices=['nexus4', 'nexus5'], default='nexus5')
    parser.add_argument('-v', '--version', dest='version', help='version', choices=['4.3', '4.4'], default='4.4')
    parser.add_argument('--variant', dest='variant', help='variant', choices=['user', 'userdebug', 'eng'], default='userdebug')

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()

def setup():
    global device, device_code_name, variant, version

    device = args.device
    if device == 'nexus4':
        device_code_name = 'mako'
    elif device == 'nexus5':
        device_code_name = 'hammerhead'
    else:
        error('The device is not supported!')
        exit(1)

    variant = args.variant
    version = args.version
    os.chdir(root_dir)

def sync():
    if not args.sync:
        return()

    execute('repo init -u https://android.googlesource.com/platform/manifest -b ' + args.sync)
    execute('repo sync')

def build():
    if not args.build:
        return()

    # Check proprietary binaries.
    backup_specific_driver_dir = backup_driver_dir + device + '/' + version + '/vendor'
    print backup_specific_driver_dir
    if not os.path.exists(backup_specific_driver_dir):
        error('Proprietary binaries dont exist')
        quit()
    execute('rm -rf vendor')
    execute('cp -rf ' + backup_specific_driver_dir + ' ./')

    start = datetime.datetime.now()
    execute(bashify('. build/envsetup.sh && lunch full_' + device_code_name + '-' + variant + ' && make -j16'))
    elapsed = (datetime.datetime.now() - start)
    info('Time elapsed to build: ' + str(elapsed.seconds) + 's')

    # Backup
    dest_dir = backup_image_dir + get_datetime() + '-' + device + '-' + variant + '/'
    os.mkdir(dest_dir)
    execute('cp ' + root_dir + 'out/target/product/' + device_code_name + '/*.img ' + dest_dir)

def flash():
    if not args.flash:
        return()

    if args.flash == 'all':
        execute('bash -c ". build/envsetup.sh && lunch full_' + device_code_name + '-' + variant + ' && fastboot -w flashall"')

if __name__ == "__main__":
    handle_option()
    setup()
    sync()
    build()
    flash()