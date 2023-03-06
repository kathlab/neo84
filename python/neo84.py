from neo84_print import nprint
import neo84_app as neo84
import neo84_task as task
import os
import setup_inf as si
import sys


def test_stack(app):
    inf = app.setup_inf.inf
    inf[si.Package.meta_data]['Author'] = 'Mr. Test'
    inf[si.Package.setup]['Platform'] = 'x64'

    inf = app.generate_inf()

    for line in inf:
        print(line)

def main():
    app = neo84.Neo84_app()
    app.print_version()

    # check for a task arg
    if (len(sys.argv) <= 1):
        print("neo84:: please add a task yaml as an argument")
        return 0

    try:
        nprint('Load task...')        

        # load task
        app.task.load_from_file(sys.argv[1])

        nprint('create package target directory...')

        # create package target dir
        app.create_package_dir()

        nprint('add registry entries...', new_line='')

        # add registry entries
        app.add_diff_reg(app.task.matrix42_diff_dir + '/Diff.inf')

        nprint('generate file lists...', add_pre_lf=True)

        # generate file lists
        app.add_files(app.task.matrix42_diff_dir)

        nprint('save setup.inf...', add_pre_lf=True)

        # save inf to file
        app.save_inf()

        nprint('copy files to target...', add_pre_lf=True)

        # copy dirs and files over from Diff dir into target dir
        # via whitelist or everything
        if (app.task.use_dir_file_whitelist):
            app.copy_diff_whitelist_data()
        else:
            app.copy_diff_data()
        
        # TODO generate tasks from scratch
        # TODO add unit tests

        nprint('Done! 🎁', add_pre_lf=True)
        
    except Exception as ex:
        print("neo84::", ex)
        return -1

if __name__ == "__main__":
    main()