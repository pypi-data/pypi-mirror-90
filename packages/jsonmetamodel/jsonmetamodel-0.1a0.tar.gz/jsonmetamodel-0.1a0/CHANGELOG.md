# Changelog
## [0.1a0]
### Added
- ADataType defines `validate(value_to_validate: Any) -> ValidationResult`
  aiming to provide an additional validation of values differently to the 
  `jsonschema` package.

## [0.0a2]
### Deprecated
- IDataType is going to be replaced by ADataType.

### Fixed
- Fixed SqlInteger to raise ValueError falsely.

### Added
- JsonObject as placeholder for dictionaries.
- JsonModel.get_blank returns a dictionary with default values.
- starting sphinx docs for mainly doctests with a simple documentation as an
  additional result.