from typing import Any


class Alx_AddonUpdater_Settings():
    """
    WARNING: git_repo defaults to the name of the addon, set the value if the two don't match

    git_engine : [str] "Github" | "GitLab" | "Bitbucket"
    git_user : [str]
    """

    _git_engine: str
    _git_user: str
    _git_repo: str

    _addon_current_version: tuple[int, int, int]
    _git_repo_private_token: Any

    def __init__(self, bl_info: dict):
        self._git_engine = "Github"
        self._git_user = "Valery-AA"
        self._git_repo = bl_info.get("name")
        self._git_repo_private_token = None

        self._addon_current_version = bl_info.get("version")

    # Choose your own username, must match website (not needed for GitLab).
    updater.user = "Valery-AA"

    # Choose your own repository, must match git name for GitHUb and Bitbucket,
    # for GitLab use project ID (numbers only).
    updater.repo = "XNALaraMesh-BL4_X"

    # updater.addon = # define at top of module, MUST be done first

    # Website for manual addon download, optional but recommended to set.
    updater.website = "https://github.com/Valery-AA/XNALaraMesh-BL4_X"

    # Addon subfolder path.
    # "sample/path/to/addon"
    # default is "" or None, meaning root
    updater.subfolder_path = ""

    # Used to check/compare versions.
    updater.current_version = bl_info["version"]

    # Optional, to hard-set update frequency, use this here - however, this
    # demo has this set via UI properties.
    # updater.set_check_interval(enabled=False, months=0, days=0, hours=0, minutes=2)

    # Optional, consider turning off for production or allow as an option
    # This will print out additional debugging info to the console
    updater.verbose = False  # make False for production default

    # Optional, customize where the addon updater processing subfolder is,
    # essentially a staging folder used by the updater on its own
    # Needs to be within the same folder as the addon itself
    # Need to supply a full, absolute path to folder
    from pathlib import Path
    updater._updater_path = str(Path.absolute(Path(update_path_fix[0])))
    # set path of updater folder, by default:
    # 			/addons/{__package__}/{__package__}_updater

    # Auto create a backup of the addon when installing other versions.
    updater.backup_current = True  # True by default

    # Sample ignore patterns for when creating backup of current during update.
    updater.backup_ignore_patterns = ["__pycache__", ".git", ".gitignore"]
    # Alternate example patterns:
    # updater.backup_ignore_patterns = [".git", "__pycache__", "*.bat", ".gitignore", "*.exe"]

    # Patterns for files to actively overwrite if found in new update file and
    # are also found in the currently installed addon. Note that by default
    # (ie if set to []), updates are installed in the same way as blender:
    # .py files are replaced, but other file types (e.g. json, txt, blend)
    # will NOT be overwritten if already present in current install. Thus
    # if you want to automatically update resources/non py files, add them as a
    # part of the pattern list below so they will always be overwritten by an
    # update. If a pattern file is not found in new update, no action is taken
    # NOTE: This does NOT delete anything proactively, rather only defines what
    # is allowed to be overwritten during an update execution.
    updater.overwrite_patterns = ["*.png", "*.jpg", "README.md", "LICENSE.txt"]
    # updater.overwrite_patterns = []
    # other examples:
    # ["*"] means ALL files/folders will be overwritten by update, was the
    #    behavior pre updater v1.0.4.
    # [] or ["*.py","*.pyc"] matches default blender behavior, ie same effect
    #    if user installs update manually without deleting the existing addon
    #    first e.g. if existing install and update both have a resource.blend
    #    file, the existing installed one will remain.
    # ["some.py"] means if some.py is found in addon update, it will overwrite
    #    any existing some.py in current addon install, if any.
    # ["*.json"] means all json files found in addon update will overwrite
    #    those of same name in current install.
    # ["*.png","README.md","LICENSE.txt"] means the readme, license, and all
    #    pngs will be overwritten by update.

    # Patterns for files to actively remove prior to running update.
    # Useful if wanting to remove old code due to changes in filenames
    # that otherwise would accumulate. Note: this runs after taking
    # a backup (if enabled) but before placing in new update. If the same
    # file name removed exists in the update, then it acts as if pattern
    # is placed in the overwrite_patterns property. Note this is effectively
    # ignored if clean=True in the run_update method.
    updater.remove_pre_update_patterns = ["*.py", "*.pyc"]
    # Note setting ["*"] here is equivalent to always running updates with
    # clean = True in the run_update method, ie the equivalent of a fresh,
    # new install. This would also delete any resources or user-made/modified
    # files setting ["__pycache__"] ensures the pycache folder always removed.
    # The configuration of ["*.py", "*.pyc"] is a safe option as this
    # will ensure no old python files/caches remain in event different addon
    # versions have different filenames or structures.

    # Allow branches like 'master' as an option to update to, regardless
    # of release or version.
    # Default behavior: releases will still be used for auto check (popup),
    # but the user has the option from user preferences to directly
    # update to the master branch or any other branches specified using
    # the "install {branch}/older version" operator.
    updater.include_branches = False

    # (GitHub only) This options allows using "releases" instead of "tags",
    # which enables pulling down release logs/notes, as well as installs update
    # from release-attached zips (instead of the auto-packaged code generated
    # with a release/tag). Setting has no impact on BitBucket or GitLab repos.
    updater.use_releases = True
    # Note: Releases always have a tag, but a tag may not always be a release.
    # Therefore, setting True above will filter out any non-annotated tags.
    # Note 2: Using this option will also display (and filter by) the release
    # name instead of the tag name, bear this in mind given the
    # skip_tag_function filtering above.

    # Populate if using "include_branches" option above.
    # Note: updater.include_branch_list defaults to ['master'] branch if set to
    # none. Example targeting another multiple branches allowed to pull from:
    # updater.include_branch_list = ['master', 'dev']
    updater.include_branch_list = None  # None is the equivalent = ['master']

    # Only allow manual install, thus prompting the user to open
    # the addon's web page to download, specifically: updater.website
    # Useful if only wanting to get notification of updates but not
    # directly install.
    updater.manual_only = False

    # Used for development only, "pretend" to install an update to test
    # reloading conditions.
    updater.fake_install = False  # Set to true to test callback/reloading.

    # Show popups, ie if auto-check for update is enabled or a previous
    # check for update in user preferences found a new version, show a popup
    # (at most once per blender session, and it provides an option to ignore
    # for future sessions); default behavior is set to True.
    updater.show_popups = True
    # note: if set to false, there will still be an "update ready" box drawn
    # using the `update_notice_box_ui` panel function.

    # Override with a custom function on what tags
    # to skip showing for updater; see code for function above.
    # Set the min and max versions allowed to install.
    # Optional, default None
    # min install (>=) will install this and higher
    updater.version_min_update = None
    # updater.version_min_update = None  # None or default for no minimum.

    # Max install (<) will install strictly anything lower than this version
    # number, useful to limit the max version a given user can install (e.g.
    # if support for a future version of blender is going away, and you don't
    # want users to be prompted to install a non-functioning addon)
    # updater.version_max_update = (9,9,9)
    updater.version_max_update = None  # None or default for no max.

    # Function defined above, customize as appropriate per repository
    updater.skip_tag = skip_tag_function  # min and max used in this function

    # Function defined above, optionally customize as needed per repository.
    updater.select_link = select_link_function

    # Recommended false to encourage blender restarts on update completion
    # Setting this option to True is NOT as stable as false (could cause
    # blender crashes).
    updater.auto_reload_post_update = True
