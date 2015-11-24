How to create packages
-----

The packaging of both the LogReader and the UI components is based on spec files found here:

 > **Path:** zipnish/log-reader/redhat/log-reader.spec
 
 > **Path:** zipnish/ui/redhat/zipnish-ui.spec 

Create your required package by using the rpmbuild command:

*Example:*
```sh
$ rpmbuild -bb specfile
```
