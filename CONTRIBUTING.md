# Contributing

Contributing to KPP_Patch will require some basic understanding of
[React Native][] and [Hermes bytecode][]. You will also need the
`KPPMainApp.js.hbc` file from a Kindle.

I have written [an article][Kindle homepage patching article] that introduces
the Hermes bytecode, as well as the steps to research and develop a new
patch—`patch_homepage_sf` which is now included in KPP_Patch.


## Disassembler/assembler

KPP_Patch uses [hbctool][]. Specifically, it uses a fork with
[hexpwn's Hermes v84 bytecode support][] merged in. It also has limited type
hints as well as some other improvements. The fork was necessary because the
maintainer has since abandoned the project, and will not reply to issues or
merge any PRs.

There is no documentation, but the I added
[type hints to the API][hbctool API], which should nonetheless prove helpful.


## Hermes bytecode

Kindles use an older version of Hermes bytecode—v84. `hbctool` supports this
version out of the box. You can find a full list of
[Hermes opcodes here][Hermes opcodes].


## Running KPP_Patch without installing

When installing the package with `pip`, `uv` or others, it will create a
`kpp_patch` executable and add it to your `PATH`. When developing locally, you
won't have that.

However, the `kpp_patch` executable is just the [kpp_patch/\_\_main\_\_.py][]
file. Run it like `PYTHONPATH=. python kpp_patch/__main__.py`. `PYTHONPATH=.`
is necessary so Python finds the `kpp_patch` package.

[If you want to learn more about `PYTHONPATH`][PYTHONPATH].


## KPP_Patch patches

You should add new patches in [kpp_patch/patcher/patches.py][patches file].
Any new patch function should have the signature
`def patch_rest_of_name(khbc: KindleHBC) -> None`. This signature and the
prefix `patch_` in the function name will ensure that it gets automatically
detected and shown in the CLI interface.

You should also add a [docstring][Python docstrings]. This will also be picked
up and shown in the CLI interface. It should follow this format:

```txt
Patch title, should be one line, and under 80 characters when possible.

Patch description, can be multiple paragraphs. Keep around 80 character lines.

See docs/patch_example.jpg
```

The last line, containing an image giving an example of what the patch does or
removes, should follow that exact same syntax, first the `See ` prefix, and
then the path to the image.


## KPP_Patch WIP patches

If you are working on a patch, and it would be beneficial to share with other
contributors or maintainers, but it's not quite ready for external people to
use just yet, you can add the suffix `_wip` to the patch name, like
`patch_new_custom_wip`.

This will make it so it doesn't show up in the CLI help output, however, if
you know the patch name, you can still pass it in the CLI, like
`--patch_new_custom_wip`, and KPP_Patch will apply the WIP patch.

Once it's ready for general use, simply removing the `_wip` suffix will cause
it to become public in the CLI.


## Keeping the README up to date

The README contains a copy of the `--help` output, as well as a list of
patches, with their docstring documentation and image of what they do.

To keep this list up to date, run the [update_readme script][] like
`python scripts/update_readme.py`. This will automatically update the `--help`
section in the README, as well as the list of patches and their documentation.

How this works is that the README.md file has `CH0`/`CH1` and `CP0`/`CP1`
comment blocks. These won't show up in the rendered Markdown file, but the
update script will update the content of these blocks. Do not update these
blocks manually in the README, and instead run the [update_readme script][].



[React Native]: https://reactnative.dev/
[Hermes bytecode]: https://reactnative.dev/docs/hermes
[Kindle homepage patching article]: https://sighery.com/posts/patching-kindle-homepage/
[hbctool]: https://github.com/Sighery/hbctool
[hexpwn's Hermes v84 bytecode support]: https://github.com/bongtrop/hbctool/pull/31
[hbctool API]: https://github.com/Sighery/hbctool/blob/8f9bd718445abc4d1068f9cf9702f79f090fc74b/hbctool/hbc/hbcbase/__init__.py#L120-L170
[Hermes opcodes]: https://p1sec.github.io/hermes-dec/opcodes_table.html
[kpp_patch/\_\_main\_\_.py]: ./kpp_patch/__main__.py
[PYTHONPATH]: https://docs.python.org/3/library/sys_path_init.html
[patches file]: ./kpp_patch/patcher/patches.py
[Python docstrings]: https://peps.python.org/pep-0287/
[update_readme script]: ./scripts/update_readme.py
