# Metaloader: A Configuration File Loader and Preprocessor

This package offers a highly configurable pipeline for loading complex configuration file hierarchies.

It provides abstractions for several stages in the configuration loading pipeline:

 - Filesystems: Files could be stored on any kind of filesystem - Local, Amazon S3, FTP etc.
 - Serialisations: Files could be in any number of formats - JSON, YAML etc.
 - Directives: Files can contain special "preprocessor directives" - Imports, Macros etc.
 - Stanza Handlers: Different top-level stanzas in the files may need to be handled and merged in a special way, or validated.



