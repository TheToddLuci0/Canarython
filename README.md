# Canarython
A simply python module to generate "Warrany Canary" type GPG signed messages. The main (read: only) benefit of this tool over using GPG directly is that it will automatically handle downloading a collection of proofs from the internet.

By default, it pulls in CNN, Fox [News](https://www.npr.org/2020/09/29/917747123/you-literally-cant-believe-the-facts-tucker-carlson-tells-you-so-say-fox-s-lawye), Proton, and BBC's latest headlines to "prove" that the message was not preprepared.
Why those three? Simple: I doubt even POTUS, UN Secretary General, and the King of England combined could get those four to agree to an op.

## Install
You will need to install [GpgME](https://gnupg.org/software/gpgme/index.html) to use this tool. On most Linux distros, it can be installed from the package manager, though that version may be slightly out of date. For example, `apt-get install python3-gpg`.

After that, simply `python3 -m pip install .`