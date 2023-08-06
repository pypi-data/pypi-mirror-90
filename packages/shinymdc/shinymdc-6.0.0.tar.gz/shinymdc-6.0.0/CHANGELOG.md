# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [6.0.0](https://github.com/jayanthkoushik/mdc/compare/v5.2.0...v6.0.0) (2021-01-05)


### ⚠ BREAKING CHANGES

* **templates:** update simple/stylish fonts

### Features

* **templates:** update simple/stylish fonts ([4a1fb44](https://github.com/jayanthkoushik/mdc/commit/4a1fb4412afa4581974508ee7ba0973613131891))


### Bug Fixes

* **templates:** enable french spacing ([9f7bfde](https://github.com/jayanthkoushik/mdc/commit/9f7bfde430ec271058385531d42ba5a15ccf6bd4))
* **templates:** set max width/height for figures ([839f216](https://github.com/jayanthkoushik/mdc/commit/839f216521a9d0cd91eefbd04f0f18c0faf9d6a2))

## [5.2.0](https://github.com/jayanthkoushik/mdc/compare/v5.1.0...v5.2.0) (2020-10-11)


### Features

* add appendix support ([0518ecf](https://github.com/jayanthkoushik/mdc/commit/0518ecfa85e65c8ffc6a14d3e6de88473feb384c))
* add template for stubs ([05868f4](https://github.com/jayanthkoushik/mdc/commit/05868f49aacf01631ea9520c7491a432c4e0497b))

## [5.1.0](https://github.com/jayanthkoushik/mdc/compare/v5.0.0...v5.1.0) (2020-10-10)


### Features

* allow disabling read from .mdc folder ([ac03a73](https://github.com/jayanthkoushik/mdc/commit/ac03a73cb908c637bf88ce636f09e2b721930a22))


### Bug Fixes

* **templates:** maintain aspect ratio of figures ([cbe0023](https://github.com/jayanthkoushik/mdc/commit/cbe002391130296c16b3781cba0f2f5c89650b04))
* **templates:** provide italics as bold for garamond ([0ddc8a9](https://github.com/jayanthkoushik/mdc/commit/0ddc8a95b39298985cd45f3509f2ff9ed74add65))
* **templates:** use mbox for names ([9e6c5c5](https://github.com/jayanthkoushik/mdc/commit/9e6c5c541ff4e5d149a77580f78ebb1ce9a67517))
* **templates:** workaround pandoc multiline tables ([cc7455b](https://github.com/jayanthkoushik/mdc/commit/cc7455bfcc21bf081f356bd2f20a91af8f88e044))
* allow endfirsthead to be absent in tables ([ea1f4d5](https://github.com/jayanthkoushik/mdc/commit/ea1f4d52860e0e0e57eb48bf194dd1bb2dcf9ecf))
* handle tables when writing to stdout ([ccb06d9](https://github.com/jayanthkoushik/mdc/commit/ccb06d9fe72ae7f9a55a6b7cb8d803208c0eb44f))

## [5.0.0](https://github.com/jayanthkoushik/mdc/compare/v4.0.0...v5.0.0) (2020-09-29)


### ⚠ BREAKING CHANGES

* do complete rehaul ([609c171](https://github.com/jayanthkoushik/mdc/commit/609c171e700a82e4511dab8a0ccaf181b59550ae))

	Major changes:
	 1. Fix table processing: use standard table env instead of longtable
	 2. Disable pandoc wrapping
	 3. Change default pandoc source format to plain markdown
	 4. Change default sans serif font from Futura to Source Pro Sans
	 5. Add functionality to two column templates for switching between
			figure/figure* and table/table*
	 6. Fine-tune float placement
	 7. Add test file test/main.md

## [4.0.0](https://github.com/jayanthkoushik/mdc/compare/v3.1.0...v4.0.0) (2020-09-08)


### ⚠ BREAKING CHANGES

* use standard-version instead of bumpversion

### Bug Fixes

* correct version import ([6aaa7a8](https://github.com/jayanthkoushik/mdc/commit/6aaa7a8b89a55b296f261ae5bc814db4bfcf4bfe))
