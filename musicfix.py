import sys, os, shutil
import tempfile, time


class MFix(object):

    def __init__(self, path):
        self.destination = path
        self.tmpdir = None

    def copy_to_tmp_dir(self):
        self.tmpdir = '/tmp/musicfix'
        shutil.copytree(self.destination, self.tmpdir)

    def copy_to_destination(self, path):
        fns = [fn for fn in sorted(os.listdir('%s/%s' % (self.tmpdir, path)))] 
        dest_dir_path = '%s/%s' % (self.destination, path)
        shutil.rmtree(dest_dir_path)
        os.mkdir(dest_dir_path)
        for name in fns:
            print ('-> %s' % name)
            dest_path = '%s/%s' % (dest_dir_path, name)
            # copy file back
            shutil.copy('%s/%s/%s' % (self.tmpdir, path, name), dest_path)
            time.sleep(1)
        pass

    def get_subdirs(self, path):
        subdirs = []
        for d in os.listdir(path):
            # ignore hidden dirs
            if d[0] == '.':
                continue
            if os.path.isdir('%s/%s' % (path, d)):
                subdirs.append(d)
        return subdirs

    def execute(self):
        self.copy_to_tmp_dir()
        for path in self.get_subdirs(self.tmpdir):
            print ("DIRECTORY '%s'" % path)
            self.copy_to_destination(path)
        shutil.rmtree(self.tmpdir)


if __name__ == '__main__':
    argv = sys.argv
    if not os.path.isdir(argv[1]):
        raise Exception('Invalid, not existing directory!')
    MFix(argv[1]).execute()
