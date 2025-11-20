%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '/etc/bash_completion.d')

Name:    crystal
Version: 1.18.2
Release: %autorelease
Summary: The Crystal Programming Language

%global bootstrap %{version}

License: ASL 2.0
URL:     https://crystal-lang.org
Source0: https://github.com/crystal-lang/crystal/archive/%{version}/crystal-%{version}.tar.gz
Source2: crystal-wrapper.sh
%if 0%{?bootstrap:1}
Source4: https://github.com/crystal-lang/crystal/releases/download/%{bootstrap}/crystal-%{bootstrap}-1-linux-x86_64.tar.gz
Source5: https://github.com/crystal-lang/crystal/releases/download/%{bootstrap}/crystal-%{bootstrap}-1-linux-aarch64.tar.gz
%endif

BuildRequires: xz
BuildRequires: tar
BuildRequires: git
BuildRequires: file
BuildRequires: make
%if !0%{?bootstrap:1}
BuildRequires: crystal < %{version}
%endif
BuildRequires: gcc-c++
BuildRequires: gc-devel >= 7.6.0
BuildRequires: llvm-devel >= 3.8
BuildRequires: findutils
BuildRequires: pcre2-devel
BuildRequires: libffi-devel
BuildRequires: libyaml-devel
BuildRequires: pkgconfig(bash-completion)
%if ! 0%{?bootstrap:1}
BuildRequires: crystal%{?_isa} < %{version}-%{release}
%endif

Requires: gc-devel >= 7.6.0
Requires: gmp-devel
Requires: pcre2-devel
Requires: zlib-devel
Requires: libffi-devel
Requires: libxml2-devel
Requires: libyaml-devel
Requires: openssl-devel

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
%autosetup -p1

%if 0%{?bootstrap:1}
%ifarch x86_64
%{__tar} -xzf %{SOURCE4} -C .
%endif
%ifarch aarch64
%{__tar} -xzf %{SOURCE5} -C .
%endif
%endif


%build
%if 0%{?bootstrap:1}
bootstrap="$(readlink -f ./crystal-%{bootstrap}*)"
binarydir=$(find "$bootstrap" -name crystal -type f -executable -exec sh -c "file -i '{}' |grep charset=binary >/dev/null" \; -print0 |xargs -0 dirname)

PATH="$binarydir:$PATH"; export PATH
%endif

export release=1
export verbose=1
export threads=%{_smp_build_ncpus}
export interpreter=1
export CXXFLAGS="%optflags"
export LLVM_CONFIG=$(find %{_bindir} -name "llvm-config*" -print -quit)
make
make docs


%install
install -D -m 755 %{SOURCE2} %{buildroot}%{_bindir}/crystal
sed -i 's|CRYSTAL_LIBRARY_PATH=/usr/lib:/usr/local/lib|CRYSTAL_LIBRARY_PATH=%{_libdir}:/usr/local/%{_lib}|' \
    %{buildroot}%{_bindir}/crystal

install -D -m 755 .build/crystal %{buildroot}%{_prefix}/lib/crystal/bin/crystal

gzip -9 man/crystal.1
install -D -m 644 man/crystal.1.gz %{buildroot}%{_mandir}/man1/crystal.1.gz

install -D -m 644 etc/completion.bash %{buildroot}%{bash_completionsdir}/crystal
install -D -m 644 etc/completion.zsh %{buildroot}%{_datadir}/zsh/site-functions/_crystal

mkdir -p %{buildroot}%{_datadir}/crystal
cp -r src %{buildroot}%{_datadir}/crystal
cp -r docs %{buildroot}%{_datadir}/crystal
cp -r samples %{buildroot}%{_datadir}/crystal


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
%autochangelog
