# Python dead batteries redistribution

Python is moving forward! Python finally started to remove dead batteries.
For more information, see [PEP 594](https://peps.python.org/pep-0594/).

If your project depends on a module that has been removed from the standard,
here is the redistribution of the dead batteries.

```shell
pip install standard-{name}  # Don't forget to add `standard-` prefix!
pip install standard-uu  # e.g. `uu` can be installed by standard-uu
```

- [aifc](https://pypi.org/project/standard-aifc/)
- [asynchat](https://pypi.org/project/standard-asynchat/)
- [asyncore](https://pypi.org/project/standard-asyncore/)
- [cgi](https://pypi.org/project/standard-cgi/)
- [cgitb](https://pypi.org/project/standard-cgitb/)
- [chunk](https://pypi.org/project/standard-chunk/)
- [crypt](https://pypi.org/project/standard-crypt/)
- [imghdr](https://pypi.org/project/standard-imghdr/)
- [mailcap](https://pypi.org/project/standard-mailcap/)
- [nntplib](https://pypi.org/project/standard-nntplib/)
- [pipes](https://pypi.org/project/standard-pipes/)
- [smtpd](https://pypi.org/project/standard-smtpd/)
- [sndhdr](https://pypi.org/project/standard-sndhdr/)
- [sunau](https://pypi.org/project/standard-sunau/)
- [telnetlib](https://pypi.org/project/standard-telnetlib/)
- [uu](https://pypi.org/project/standard-uu/)
- [xdrlib](https://pypi.org/project/standard-xdrlib/)


## Contribution guideline

Please do *NOT* submit any new features or any compatibility work.
This repository is archiving the old standard library installable via pip.
If you find any broken packages or missing features, please look for other projects that are actively developing alternative packages or fork this project.

Please report any bug or submit patches if you encounter any issues with package generation.
Patches related to files under `template` and `scripts` are welcome!

## To Python developers

I'm really happy that this is happening! I hope that Python development and maintenance will be less of a burden as a result of this decision. At the same time, I'd love to encourage Python developers to more actively deprecate less core-feature related batteries and push them out to PyPI.

I hope the Python team will make the similar packages. If you could take over or do something similar to what this repository does, and release at least one version, the final version of removed standard libraries to PyPI, that would be amazing! Unfortunately, this isn't able to work from third-party due to the [package name rule](https://pypi.org/help/#project-name). I'll do my best to support you if you need it.

Then please make `__import__` notify users when failed to import removed standard libraries that they are installable via PIP. This step will enhance user experience. But the first step is necessary because Python can't advertise third party libraries in binary due to security issues.

I know it might sound like more maintenance work, but it's not as bad as it seems! `PEP 594` strictly defined the really dead libraries. On the other hand, Python developers still have to maintain a huge part of the old standard libraries, which were added in the pre-PyPI era.

It's not easy to tell users "We will deprecate this library. Please fork or go to find another library."  I know it's not the most pleasant thing to do. Preparing a backup will be a bit more nice. Now telling "We will remove this library from standard library, but you can install it via PIP!" will be a lot easier. The only additional burden for users will be the Internet with SSL.

There could be one more step - though this is a rejected idea in PEP 594. If we can get users to install the old standard packages via PIP, we can also get them to install less core-language libraries as separatedly distributing first-party libraries. Libraries that have users but aren't necessarily standard libraries can be turned into non-standard libraries.
I'm not sure if this is the best way, but it will give developers the option to choose whether or not to do.

I really hope that finally Python developers could decide to remove even more batteries in future.
