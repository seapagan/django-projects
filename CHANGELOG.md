# Changelog

This is an auto-generated log of all the changes that have been made to the
project since the first release, with the latest changes at the top.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased](https://github.com/seapagan/django-projects/tree/HEAD)

These are the changes that have been merged to the repository since the last
release.

Everything in this section will be included in the next official release.

**New Features**

- Add a noscript block and fix some issues with theme dropdown ([#35](https://github.com/seapagan/django-projects/pull/35)) by [seapagan](https://github.com/seapagan)

**Testing**

- Add tests to the application ([#40](https://github.com/seapagan/django-projects/pull/40)) by [seapagan](https://github.com/seapagan)

**Security**

- Update dependencies and pre-commit tool versions to clear some security issues ([#53](https://github.com/seapagan/django-projects/pull/53)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix custom error pages (bad base template path) ([#46](https://github.com/seapagan/django-projects/pull/46)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Improve header formatting and sizes ([#38](https://github.com/seapagan/django-projects/pull/38)) by [seapagan](https://github.com/seapagan)
- Locally host HTMX and Alpine.js instead of using CDN ([#37](https://github.com/seapagan/django-projects/pull/37)) by [seapagan](https://github.com/seapagan)
- Refactor the layout slightly to reuse templates between apps. ([#36](https://github.com/seapagan/django-projects/pull/36)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump django from 5.2 to 5.2.1 ([#48](https://github.com/seapagan/django-projects/pull/48)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Update astral-sh/setup-uv action to v6 ([#44](https://github.com/seapagan/django-projects/pull/44)) by [renovate[bot]](https://github.com/apps/renovate)
- Bump h11 from 0.14.0 to 0.16.0 ([#43](https://github.com/seapagan/django-projects/pull/43)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump django from 5.1.7 to 5.1.8 ([#41](https://github.com/seapagan/django-projects/pull/41)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/django-projects/compare/1.0.0...HEAD) | [`Diff`](https://github.com/seapagan/django-projects/compare/1.0.0...HEAD.diff) | [`Patch`](https://github.com/seapagan/django-projects/compare/1.0.0...HEAD.patch)

## [1.0.0](https://github.com/seapagan/django-projects/releases/tag/1.0.0) (March 29, 2025)

**Initial release.**

This release is the first official release and is considered feature-complete
at this time in that it contains everything I intended in the initial planning.

**Merged Pull Requests**

- Revert "Migrate to hCaptcha" ([#28](https://github.com/seapagan/django-projects/pull/28)) by [seapagan](https://github.com/seapagan)

**New Features**

- Make the 'about' section dynamic ([#33](https://github.com/seapagan/django-projects/pull/33)) by [seapagan](https://github.com/seapagan)
- Adjust some dynamic features ([#32](https://github.com/seapagan/django-projects/pull/32)) by [seapagan](https://github.com/seapagan)
- Customize the  'collectstatic' to build/compress our assets ([#31](https://github.com/seapagan/django-projects/pull/31)) by [seapagan](https://github.com/seapagan)
- Add custom error pages ([#29](https://github.com/seapagan/django-projects/pull/29)) by [seapagan](https://github.com/seapagan)
- Migrate to hCaptcha ([#27](https://github.com/seapagan/django-projects/pull/27)) by [seapagan](https://github.com/seapagan)
- Add pagination on demand to the project list ([#26](https://github.com/seapagan/django-projects/pull/26)) by [seapagan](https://github.com/seapagan)
- Server side filtering of projects ([#25](https://github.com/seapagan/django-projects/pull/25)) by [seapagan](https://github.com/seapagan)
- Hide projects button if no projects ([#24](https://github.com/seapagan/django-projects/pull/24)) by [seapagan](https://github.com/seapagan)
- Add GitHub actions for linting and enable Renovate Bot ([#21](https://github.com/seapagan/django-projects/pull/21)) by [seapagan](https://github.com/seapagan)
- Add optional secure proxy settings. ([#20](https://github.com/seapagan/django-projects/pull/20)) by [seapagan](https://github.com/seapagan)
- Add a flag to enable/disable admin ip protection ([#19](https://github.com/seapagan/django-projects/pull/19)) by [seapagan](https://github.com/seapagan)
- Add some security to the Admin pages ([#18](https://github.com/seapagan/django-projects/pull/18)) by [seapagan](https://github.com/seapagan)
- Add optional Postgresql configuration ([#17](https://github.com/seapagan/django-projects/pull/17)) by [seapagan](https://github.com/seapagan)
- Add production settings and hardening ([#16](https://github.com/seapagan/django-projects/pull/16)) by [seapagan](https://github.com/seapagan)
- Implement giving projects a priority. ([#15](https://github.com/seapagan/django-projects/pull/15)) by [seapagan](https://github.com/seapagan)
- Enable optional caching ([#14](https://github.com/seapagan/django-projects/pull/14)) by [seapagan](https://github.com/seapagan)
- Make skills dynamic from database ([#13](https://github.com/seapagan/django-projects/pull/13)) by [seapagan](https://github.com/seapagan)
- Add dark mode ([#12](https://github.com/seapagan/django-projects/pull/12)) by [seapagan](https://github.com/seapagan)
- Add a simple header ([#11](https://github.com/seapagan/django-projects/pull/11)) by [seapagan](https://github.com/seapagan)
- Ensure project GitHub stats are updated on create or update ([#10](https://github.com/seapagan/django-projects/pull/10)) by [seapagan](https://github.com/seapagan)
- Add site configuration table ([#9](https://github.com/seapagan/django-projects/pull/9)) by [seapagan](https://github.com/seapagan)
- Send an email on contact submission ([#8](https://github.com/seapagan/django-projects/pull/8)) by [seapagan](https://github.com/seapagan)
- Add links from hero section to other sections ([#7](https://github.com/seapagan/django-projects/pull/7)) by [seapagan](https://github.com/seapagan)
- Refactor how we get and store the github stats ([#6](https://github.com/seapagan/django-projects/pull/6)) by [seapagan](https://github.com/seapagan)
- Switch to my dedicated library for http response codes ([#5](https://github.com/seapagan/django-projects/pull/5)) by [seapagan](https://github.com/seapagan)
- Add the (hardcoded) about pages ([#4](https://github.com/seapagan/django-projects/pull/4)) by [seapagan](https://github.com/seapagan)
- Add a contact form ([#3](https://github.com/seapagan/django-projects/pull/3)) by [seapagan](https://github.com/seapagan)
- Add tag functionality to projects ([#2](https://github.com/seapagan/django-projects/pull/2)) by [seapagan](https://github.com/seapagan)
- Add GitHub stats for each project. ([#1](https://github.com/seapagan/django-projects/pull/1)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Ensure correct js file is added to context for all views ([#34](https://github.com/seapagan/django-projects/pull/34)) by [seapagan](https://github.com/seapagan)

---
*This changelog was generated using [github-changelog-md](http://changelog.seapagan.net/) by [Seapagan](https://github.com/seapagan)*
