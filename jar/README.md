# Published schemas jar

For JVM projects that need to consume this repository's schemas,
we provide packaging of the project as a Java `.jar` file that we
upload to our maven repositories in S3.

## Prerequisites

There's not much need to build and test this jar building process
locally, so we don't provide much instruction for setting up
a local environment. You'll need Java, `make`, and `mvn` installed
for the following steps to work.

## Building and exploring the jar

To build the jar, run:

```
cd jar/
make jar
```

If you want to investigate the contents of the jar, run:

```
$ jar -tf target/mozilla-pipeline-schemas-1.0-SNAPSHOT.jar
META-INF/MANIFEST.MF
META-INF/
schemas/
schemas/heka/
schemas/heka/pioneer-study/
schemas/heka/telemetry/
...
```

## Using the jar

A versioned jar is published for each tag on this repository.
To make the `v0.10.0` tagged schemas available in a Maven project, 
add the following to your `pom.xml` dependencies:

```xml
        <dependency>
            <groupId>com.mozilla.telemetry</groupId>
            <artifactId>mozilla-pipeline-schemas</artifactId>
            <version>0.10.0</version>
        </dependency>
```

You should then be able to access the schemas in your project 
using the ClassLoader directly or via a tool like Guava's
`Resources.getResource()`:

```java
final URL url = Resources.getResource("/schemas/telemetry/event/event.4.schema.json")
```

If you're doing development on this repo and want to test the effects
in other projects, you can compile and install your current development
version locally via:

```bash
# Builds the jar and installs in your local ~/.m2
mvn clean install
```

Then configure your consuming project to use the `1.0-SNAPSHOT` version:

```xml
        <dependency>
            <groupId>com.mozilla.telemetry</groupId>
            <artifactId>mozilla-pipeline-schemas</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
```
