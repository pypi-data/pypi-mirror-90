import pkg_upload
f = open("README.md", "r", encoding="utf-8")
long = f.read()
f.close()
pkg_upload.package(
    pkg_name="crazyweirdpackage",
    author="PkgDev",
    email="example@example.com",
    version="0.0.1",
    short_description=
    "a very very very very very very very very simle calculator.",
    long_description=long,
    github_url="https://github.com",
    python_requirment=">=3.6")
