# u2_flutter API Contract

## Version: 0.1.0 (Experimental)

This document establishes the official API contract for `u2_flutter`, defining stability tiers for locators, actions, utilities, and future enhancement paths.

## Stable APIs (Will not change without major version bump)
- `Flutter(d)` - Instantiate the Flutter driver plugin wrapper over a `uiautomator2` device instance.
- `Flutter.find_by_key(key)` - Find widget by key (returns a deferred `FlutterElement`).
- `Flutter.find_by_text(text)` - Find widget by exact text content match.
- `FlutterElement.tap()` - Tap/click on the target widget.
- `FlutterElement.enter_text(text)` - Input text characters into the target widget (e.g. text field).
- `FlutterElement.get_text()` - Retrieve the text attribute of the target widget.

## Experimental APIs (May change in minor versions)
- `Flutter.find_by_type(type)` - Locate widgets filtering by their runtime type (e.g. `ElevatedButton`).
- `Flutter.scroll(finder, dx, dy)` - Scroll lists or scrollable elements by pixel offsets.
- `Flutter.wait_for(finder, timeout)` - Bounded wait loops verifying element existence on screen.

## Unsupported (Planned for future)
- **iOS support**: Currently restricted to Android ADB platforms.
- **ByTooltip finder**: Locating widgets by tooltip properties.
- **BySemanticsLabel finder**: Locating widgets by accessibility/semantics labels.
- **Screenshot capture**: Custom viewport capture (relying on native system screenshot captures instead).

## Versioning Policy
- **MAJOR**: Breaking changes to stable locator methods or action signatures.
- **MINOR**: Additions of new locate properties, experimental features, or helper decorators.
- **PATCH**: Internal optimizations, bug fixes, port resolution improvements, and performance tweaks.
