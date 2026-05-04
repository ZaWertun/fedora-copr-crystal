%define molinillo_version 0.2.0

Name:    shards
Version: 0.20.0
Release: 2%{?dist}
Summary: Dependency manager for the Crystal language

License: ASL 2.0
URL:     https://github.com/crystal-lang/shards
Source0: https://github.com/crystal-lang/shards/archive/v%{version}/shards-%{version}.tar.gz
Source1: https://github.com/crystal-lang/crystal-molinillo/archive/v%{molinillo_version}/crystal-molinillo-%{molinillo_version}.tar.gz

# --- BUILD DEPENDENCIES ---
BuildRequires: gcc
BuildRequires: make
# Explicitly require the Crystal compiler
BuildRequires: crystal
# Required for man page generation
BuildRequires: asciidoctor
# Required for linking (shards uses YAML heavily)
BuildRequires: libyaml-devel
BuildRequires: pcre2-devel
BuildRequires: openssl-devel

# --- RUNTIME DEPENDENCIES ---
# Shards delegates to git for cloning
Requires: git
# Shards often runs 'postinstall' hooks which execute crystal code
Requires: crystal

%description
Dependency manager for the Crystal language.

%prep
%autosetup -p1
# Vendor molinillo manually as per upstream structure
mkdir -p lib/molinillo
tar -xf %{SOURCE1} --strip-components=1 -C lib/molinillo

%build
# Crystal build flags
export release=1
# Force static linking for portability or standard dynamic linking?
# Standard dynamic linking is preferred for Fedora packages.
# The Makefile usually handles 'release=1' by adding --release --no-debug
make bin/shards

# Generate Man Pages
make docs

%install
# Install binary
install -D -m 0755 bin/shards %{buildroot}%{_bindir}/shards

# Install man pages
install -D -m 0644 man/shards.1 %{buildroot}%{_mandir}/man1/shards.1
install -D -m 0644 man/shard.yml.5 %{buildroot}%{_mandir}/man5/shard.yml.5

%check
make test

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/shards
%{_mandir}/man1/shards.1*
%{_mandir}/man5/shard.yml.5*

%changelog
* Sun May 03 2026 Rénich Bon Ćirić <renich@woralelandia.com> - 0.20.0-2
- Fix dependencies and remove legacy filtering scripts
- Simplified docs generation

* Thu Apr 02 2026 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.20.0-1
- version 0.20.0

* Wed Feb 05 2025 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.19.1-1
- version 0.19.1

* Thu May 16 2024 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.18.0-1
- version 0.18.0

* Fri Apr 14 2023 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.17.3-1
- version 0.17.3

* Tue Jan 10 2023 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.17.2-1
- version 0.17.2

* Fri Mar 25 2022 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.17.0-1
- version 0.17.0

* Wed Oct 13 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.16.0-1
- version 0.16.0

* Wed Jun 30 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.15.0-1
- version 0.15.0

* Thu Mar 11 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.14.1-1
- version 0.14.1

* Wed Feb 24 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.14.0-1
- version 0.14.0, crystal-molinillo-0.2.0

* Sun Jan 24 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.13.0-1
- version 0.13.0

* Fri Aug 07 2020 Yaroslav Sidlovsky <zawertun@otl.ru> - 0.12.0-1
- version 0.12.0

* Tue Jun 09 2020 Yaroslav Sidlovsky <zawertun@otl.ru> - 0.11.1-1
- version 0.11.1

* Sat Jun 06 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.11.0-1
- version 0.11.0

* Tue Apr 07 2020 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.10.0-1
- version 0.10.0

* Tue Jun 18 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.9.0-8
- version 0.9.0

* Wed May 08 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.9.0~rc2-7
- version 0.9.0.rc2

* Sat Feb 09 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.9.0~rc1-6
- version 0.9.0.rc1

* Thu Jan 31 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.9.0~beta-5
- version 0.9.0.beta

* Wed Jun 20 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.8.1-4
- version 0.8.1

* Fri Jun 15 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.8.0-3
- `git` added to requires

* Thu Jun 14 2018 Yaroslav Sidlovsky <zawertun@gmail.com> - 0.8.0-2
- version 0.8.0
