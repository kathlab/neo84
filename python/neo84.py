import os
import neo84_app as neo84
import setup_inf as sinf

def main():
    app = neo84.Neo84_app()
    app.print_version()
    inf = app.setup_inf.inf

    inf[sinf.Package.meta_data]['Author'] = 'Mr. Test'
    inf[sinf.Package.setup]['Platform'] = 'x64'

    app.print_inf()

if __name__ == "__main__":
    main()