plugins {
    java
    id("org.springframework.boot") version "3.0.5"
    id("io.spring.dependency-management") version "1.1.0"
}

group = "bmstu"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_17

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter")
    implementation("com.fasterxml.jackson.core:jackson-annotations:2.14.2")
    implementation("com.fasterxml.jackson.core:jackson-databind:2.14.2")
    implementation("com.google.code.gson:gson:2.10.1")


    //LOMBOK Dependencies
    annotationProcessor("org.projectlombok:lombok")
    compileOnly("org.projectlombok:lombok")
    testAnnotationProcessor("org.projectlombok:lombok")
    testCompileOnly("org.projectlombok:lombok")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.assertj:assertj-core:3.24.2")
    testImplementation("junit:junit")

    testCompileOnly("org.junit.jupiter:junit-jupiter-params")

    //testImplementation("org.junit.jupiter:junit-jupiter-api")
    //testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine")
}

tasks.withType<Test> {
    useJUnitPlatform()
}


