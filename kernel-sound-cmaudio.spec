#
# Conditional build:
%bcond_without	dist_kernel		# without distribution kernel
#
%define		_orig_name	cmaudio

%define	_rel	1
Summary:	 C-Media Linux Driver
Summary(pl.UTF-8):	Sterowniki dla Linuksa dla kart dźwiękowych opartych na C-Media
Name:		kernel-sound-%{_orig_name}
Version:	070
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.cmediadrivers.info/driver/Linux/Ac97/%{_orig_name}-%{version}.tar.bz2
# Source0-md5:	60cc9412652205d0cfc827899298b68e
# Patch0:		%{_orig_name}-Makefile.patch
# Patch1:		%{name}-types.patch
URL:		http://www.cmediadrivers.info/driver/Linux/Ac97/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
Provides:	cmiaudio
ExclusiveArch:	%{ix86}
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
C-Media Linux Driver.

%description -l pl.UTF-8
Sterowniki do kart dźwiękowych opartych na C-Media.

%prep
%setup -q -n %{_orig_name}
#%patch0 -p1
#%patch1 -p1

cat > Makefile <<'EOF'
obj-m := cmaudio.o
cmaudio-objs := ali_5451.o ati.o cmi9738.o cmi9739.o cmi9761.o intel_ichx.o main.o sis_7018.o via_82cxxx.o
EOF

%build
%build_kernel_modules -C . -m cmaudio

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m cmaudio -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc Readme.txt
/lib/modules/%{_kernel_ver}/misc/*
