%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '/etc/bash_completion.d')

Name:    crystal
Version: 1.0.0
Release: 2%{?dist}
Summary: The Crystal Programming Language

%global bootstrap %{version}

License: ASL 2.0
URL:     https://crystal-lang.org
Source0: https://github.com/crystal-lang/crystal/archive/%{version}/crystal-%{version}.tar.gz
Source1: filter-requires.sh
Source2: crystal-wrapper.sh
%if 0%{?bootstrap:1}
Source4: https://github.com/crystal-lang/crystal/releases/download/%{bootstrap}/crystal-%{bootstrap}-1-linux-x86_64.tar.gz
%endif

%define    _use_internal_dependency_generator 0
%define    __find_requires %{SOURCE1}

BuildRequires: xz
BuildRequires: tar
BuildRequires: git
BuildRequires: file
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: gc-devel >= 7.6.0
%if 0%{?fedora}
%if 0%{?fedora} < 32
BuildRequires: llvm7.0-devel
%endif
%if 0%{?fedora} == 32
BuildRequires: llvm-devel >= 3.8
%endif
%if 0%{?fedora} >= 33
BuildRequires: llvm10-devel
%endif
%else
BuildRequires: llvm-devel >= 3.8
%endif
BuildRequires: findutils
BuildRequires: pcre-devel
BuildRequires: libyaml-devel
BuildRequires: libevent-devel
BuildRequires: pkgconfig(bash-completion)
%if ! 0%{?bootstrap:1}
BuildRequires: crystal
%endif

Requires: gc-devel >= 7.6.0
Requires: gmp-devel
Requires: pcre-devel
Requires: zlib-devel
Requires: libxml2-devel
Requires: libyaml-devel
Requires: openssl-devel
Requires: libevent-devel

%description
Crystal is a programming language with the following goals:
 + Have a syntax similar to Ruby (but compatibility with it is not a goal).
 + Be statically type-checked, but without having to specify the type of variables or method arguments.
 + Be able to call C code by writing bindings to it in Crystal.
 + Have compile-time evaluation and generation of code, to avoid boilerplate code.
 + Compile to efficient native code.


%package docs
Summary: Documentation for the Crystal Programming Language
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description docs
%{summary}.


%package samples
Summary: Sample code for the Crystal Programming Language
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description samples
%{summary}.


%prep
%autosetup

%if 0%{?bootstrap:1}
%ifarch x86_64
%{__tar} -xzf %{SOURCE4} -C .
%endif
%endif


%build
%if 0%{?bootstrap:1}
bootstrap="$(readlink -f ./crystal-%{bootstrap}*)"
binarydir=$(find "$bootstrap" -name crystal -type f -executable -exec sh -c "file -i '{}' |grep charset=binary >/dev/null" \; -print0 |xargs -0 dirname)

PATH="$binarydir:$PATH"; export PATH
%endif

export LLVM_CONFIG=$(find %{_bindir} -name "llvm-config*" -print -quit)
%{__make} progress=true %{?_smp_mflags}
%{__make} docs


%install
%{__install} -D -m 755 %{SOURCE2} %{buildroot}%{_bindir}/crystal
%{__sed} -i 's|CRYSTAL_LIBRARY_PATH=/usr/lib:/usr/local/lib|CRYSTAL_LIBRARY_PATH=%{_libdir}:/usr/local/%{_lib}|' \
    %{buildroot}%{_bindir}/crystal

%{__install} -D -m 755 .build/crystal %{buildroot}%{_prefix}/lib/crystal/bin/crystal

%{__gzip} -9 man/crystal.1
%{__install} -D -m 644 man/crystal.1.gz %{buildroot}%{_mandir}/man1/crystal.1.gz

%{__install} -D -m 644 etc/completion.bash %{buildroot}%{bash_completionsdir}/crystal
%{__install} -D -m 644 etc/completion.zsh %{buildroot}%{_datadir}/zsh/site-functions/_crystal

%{__mkdir} -p %{buildroot}%{_datadir}/crystal
%{__cp} -r src %{buildroot}%{_datadir}/crystal
%{__cp} -r docs %{buildroot}%{_datadir}/crystal
%{__cp} -r samples %{buildroot}%{_datadir}/crystal


%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/crystal
%{_prefix}/lib/crystal/bin/crystal
%{_mandir}/man1/crystal.1.gz
%{bash_completionsdir}/crystal
%{_datadir}/zsh/site-functions/_crystal
%{_datadir}/crystal/src


%files docs
%dir %{_datadir}/crystal/docs/
%{_datadir}/crystal/docs/*


%files samples
%dir %{_datadir}/crystal/samples/
%{_datadir}/crystal/samples/*


%changelog
* Wed Jun 30 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 1.0.0-2
- rebuild

* Mon Mar 22 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 1.0.0-1
- version 1.0.0

* Tue Feb 02 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.36.1-1
- version 0.36.1

* Tue Jan 26 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.36.0-1
- version 0.36.0

* Fri Jun 19 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.35.1-1
- version 0.35.1

* Wed Jun 10 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.35.0-1
- version 0.35.0

* Sat May 09 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.34.0-2
- libxml2-devel added to requires

* Tue Apr 07 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.34.0-1
- version 0.34.0

* Sat Feb 15 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.33.0-1
- version 0.33.0

* Wed Dec 18 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.32.1-1
- version 0.32.1

* Thu Dec 12 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.32.0-1
- version 0.32.0

* Fri Nov 15 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.31.1-27
- llvm8.0

* Tue Oct 01 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.31.1-26
- version 0.31.1

* Tue Sep 24 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.31.0-25
- version 0.31.0

* Mon Aug 12 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.30.1-24
- version 0.30.1

* Fri Aug 02 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.30.0-23
- version 0.30.0, using llvm 8.0 to build

* Wed Jun 05 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.29.0-22
- fix: correct lib path for x86_64 arch (see issue #5738)

* Wed Jun 05 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.29.0-21
- version 0.29.0

* Wed May 08 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.28.0-20
- use llvm6.0 on Fedora 30

* Thu Apr 18 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.28.0-19
- added patch to build with llvm 7

* Thu Apr 18 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.28.0-18
- version 0.28.0

* Sat Mar 09 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.27.2-17
- fix: gmp-devel added to requires

* Wed Feb 06 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.27.2-16
- version 0.27.2

* Fri Feb 01 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.27.1-15
- fix: %%dir directive removed

* Thu Jan 31 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.27.1-14
- version 0.27.1

* Fri Nov 02 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.27.0-13
- fix: not all docs files was included

* Fri Nov 02 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.27.0-12
- version 0.27.0

* Tue Aug 28 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.26.1-11
- version 0.26.1

* Tue Aug 21 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.26.0-10
- fixed building on Fedora 29

* Fri Aug 10 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.26.0-9
- version 0.26.0

* Thu Jun 28 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.25.1-8
- version 0.25.1

* Mon Jun 18 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.25.0-7
- arch of subpackages `docs` and `samples` set to `noarch`

* Fri Jun 15 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.25.0-6
- wrapper script fixed

* Fri Jun 15 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.25.0-5
- version 0.25.0

