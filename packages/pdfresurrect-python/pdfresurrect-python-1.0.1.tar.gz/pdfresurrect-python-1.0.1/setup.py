from setuptools import setup, Extension
from distutils.command.build_ext import build_ext as build_ext_orig


class CTypesExtension(Extension):
    pass


class build_ext(build_ext_orig):

    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypesExtension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super().get_ext_filename(ext_name)


setup(
    name="pdfresurrect-python",
    version="1.0.1",
    packages=["pdfresurrect"],
    ext_modules=[
        CTypesExtension(
            "pdfresurrect.pdf",
            ["pdfresurrect/pdf.c",
             "pdfresurrect/main.c",
             "pdfresurrect/include/pdf.h",
             "pdfresurrect/include/main.h"],
            include_dirs=['pdfresurrect/include'],
            extra_compile_args=['-fPIC']
        ),
    ],
    cmdclass={'build_ext': build_ext},
)