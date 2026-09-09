import os
import zipfile

project_name = "mismo-transformer-service"
base_dir = f"/tmp/{project_name}_complete"
os.makedirs(base_dir, exist_ok=True)

# Define full directory structure including maven wrapper, docs, configs, exception handling, DTOs, controllers, services
dirs = [
    f"{base_dir}/src/main/java/com/example/mismo",
    f"{base_dir}/src/main/java/com/example/mismo/config",
    f"{base_dir}/src/main/java/com/example/mismo/controller",
    f"{base_dir}/src/main/java/com/example/mismo/dto",
    f"{base_dir}/src/main/java/com/example/mismo/exception",
    f"{base_dir}/src/main/java/com/example/mismo/service",
    f"{base_dir}/src/main/resources/schemas",
    f"{base_dir}/src/main/resources/xslt",
    f"{base_dir}/src/test/java/com/example/mismo/controller",
    f"{base_dir}/src/test/java/com/example/mismo/service",
    f"{base_dir}/src/test/resources/samples",
    f"{base_dir}/.mvn/wrapper"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. pom.xml
pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.3</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>mismo-transformer-service</artifactId>
    <version>1.0.0</version>
    <name>mismo-transformer-service</name>
    <description>Production-ready Spring Boot microservice transforming MISMO XML to JSON with XSD validation and XSLT engine</description>

    <properties>
        <java.version>17</java.version>
        <saxon.version>12.4</saxon.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Starter Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Boot Actuator for health checks and metrics -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- Saxon-HE for modern XSLT 2.0 / 3.0 processing -->
        <dependency>
            <groupId>net.sf.saxon</groupId>
            <artifactId>Saxon-HE</artifactId>
            <version>${saxon.version}</version>
        </dependency>

        <!-- Jackson Databind for JSON processing -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
        </dependency>

        <!-- Test Suite -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""

# 2. mvnw script (minimal standard executable wrapper script)
mvnw_sh = """#!/bin/sh
exec mvn "$@"
"""

# 3. application.properties & application.yml
app_yml = """server:
  port: 8080

spring:
  application:
    name: mismo-transformer-service

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: always

mismo:
  default-profile: mismo-3.4
  auto-detect-version: true
"""

# 4. ErrorResponse DTO
error_dto = """package com.example.mismo.dto;

import java.time.Instant;

public class ErrorResponse {
    private String error;
    private String details;
    private Instant timestamp;
    private int status;

    public ErrorResponse() {
        this.timestamp = Instant.now();
    }

    public ErrorResponse(String error, String details, int status) {
        this.error = error;
        this.details = details;
        this.status = status;
        this.timestamp = Instant.now();
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }
}
"""

# 5. Custom Exceptions
validation_ex = """package com.example.mismo.exception;

public class MismoValidationException extends RuntimeException {
    public MismoValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}
"""

profile_ex = """package com.example.mismo.exception;

public class UnsupportedProfileException extends RuntimeException {
    public UnsupportedProfileException(String message) {
        super(message);
    }
}
"""

transformation_ex = """package com.example.mismo.exception;

public class MismoTransformationException extends RuntimeException {
    public MismoTransformationException(String message, Throwable cause) {
        super(message, cause);
    }
}
"""

# 6. Global Exception Handler
global_handler = """package com.example.mismo.exception;

import com.example.mismo.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MismoValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MismoValidationException ex) {
        ErrorResponse response = new ErrorResponse(
                "XSD Validation Failed",
                ex.getMessage(),
                HttpStatus.BAD_REQUEST.value()
        );
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @ExceptionHandler(UnsupportedProfileException.class)
    public ResponseEntity<ErrorResponse> handleUnsupportedProfileException(UnsupportedProfileException ex) {
        ErrorResponse response = new ErrorResponse(
                "Unsupported MISMO Profile",
                ex.getMessage(),
                HttpStatus.BAD_REQUEST.value()
        );
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @ExceptionHandler(MismoTransformationException.class)
    public ResponseEntity<ErrorResponse> handleTransformationException(MismoTransformationException ex) {
        ErrorResponse response = new ErrorResponse(
                "Transformation Error",
                ex.getMessage(),
                HttpStatus.INTERNAL_SERVER_ERROR.value()
        );
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        ErrorResponse response = new ErrorResponse(
                "Internal Server Error",
                ex.getMessage(),
                HttpStatus.INTERNAL_SERVER_ERROR.value()
        );
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
"""

# 7. MismoDetector Helper
detector_java = """package com.example.mismo.service;

import org.springframework.stereotype.Component;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamReader;
import java.io.StringReader;

@Component
public class MismoProfileDetector {

    private final XMLInputFactory inputFactory;

    public MismoProfileDetector() {
        this.inputFactory = XMLInputFactory.newInstance();
        // Secure against XXE attacks
        this.inputFactory.setProperty(XMLInputFactory.SUPPORT_DTD, false);
        this.inputFactory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);
    }

    /**
     * Inspects the root element and attributes to auto-detect the MISMO profile
     * if no explicit profile header was specified.
     */
    public String detectProfile(String xmlPayload, String fallbackProfile) {
        if (xmlPayload == null || xmlPayload.isBlank()) {
            return fallbackProfile;
        }

        try {
            XMLStreamReader reader = inputFactory.createXMLStreamReader(new StringReader(xmlPayload));
            while (reader.hasNext()) {
                int event = reader.next();
                if (event == XMLStreamConstants.START_ELEMENT) {
                    String rootLocalName = reader.getLocalName();

                    if ("CLOSING_DOCUMENT".equalsIgnoreCase(rootLocalName)) {
                        return "mismo-closing";
                    }

                    if ("MESSAGE".equalsIgnoreCase(rootLocalName)) {
                        String versionAttr = reader.getAttributeValue(null, "MISMOVersionID");
                        if (versionAttr != null && !versionAttr.isBlank()) {
                            return "mismo-" + versionAttr.trim();
                        }
                        return "mismo-3.4";
                    }

                    break;
                }
            }
        } catch (Exception ignored) {
            // If stream inspection fails, return fallback
        }

        return fallbackProfile != null ? fallbackProfile : "mismo-3.4";
    }
}
"""

# 8. MismoTransformationService.java
service_java = """package com.example.mismo.service;

import com.example.mismo.exception.MismoTransformationException;
import com.example.mismo.exception.MismoValidationException;
import com.example.mismo.exception.UnsupportedProfileException;
import net.sf.saxon.s9api.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.xml.sax.SAXException;

import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class MismoTransformationService {

    private static final Logger log = LoggerFactory.getLogger(MismoTransformationService.class);

    private final ConcurrentHashMap<String, Schema> schemaCache = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<String, XsltExecutable> xsltCache = new ConcurrentHashMap<>();
    private final Processor saxonProcessor = new Processor(false);

    /**
     * Validates XML against the schema registered for the profile.
     */
    public void validateXml(String xmlPayload, String profile) {
        try {
            Schema schema = schemaCache.computeIfAbsent(profile, key -> {
                try {
                    SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
                    factory.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
                    factory.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");

                    ClassPathResource res = new ClassPathResource("schemas/" + key + ".xsd");
                    if (!res.exists()) {
                        throw new UnsupportedProfileException("XSD schema not found for profile: " + key);
                    }
                    try (InputStream is = res.getInputStream()) {
                        return factory.newSchema(new StreamSource(is));
                    }
                } catch (UnsupportedProfileException e) {
                    throw e;
                } catch (Exception e) {
                    throw new UnsupportedProfileException("Unable to load XSD for profile: " + key + ": " + e.getMessage());
                }
            });

            Validator validator = schema.newValidator();
            validator.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
            validator.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
            validator.validate(new StreamSource(new StringReader(xmlPayload)));

        } catch (SAXException e) {
            log.warn("XML schema validation failed for profile {}: {}", profile, e.getMessage());
            throw new MismoValidationException(e.getMessage(), e);
        } catch (IOException e) {
            log.error("I/O error during XML validation for profile {}: {}", profile, e.getMessage());
            throw new MismoTransformationException("I/O error during validation: " + e.getMessage(), e);
        }
    }

    /**
     * Transforms XML to JSON using XSLT 3.0 compiled for the profile.
     */
    public String transformToJson(String xmlPayload, String profile) {
        try {
            XsltExecutable executable = xsltCache.computeIfAbsent(profile, key -> {
                try {
                    ClassPathResource res = new ClassPathResource("xslt/" + key + ".xsl");
                    if (!res.exists()) {
                        throw new UnsupportedProfileException("XSL stylesheet not found for profile: " + key);
                    }
                    XsltCompiler compiler = saxonProcessor.newXsltCompiler();
                    try (InputStream is = res.getInputStream()) {
                        return compiler.compile(new StreamSource(is));
                    }
                } catch (UnsupportedProfileException e) {
                    throw e;
                } catch (Exception e) {
                    throw new UnsupportedProfileException("Unable to compile XSL for profile: " + key + ": " + e.getMessage());
                }
            });

            Xslt30Transformer transformer = executable.load30();
            StringWriter outputWriter = new StringWriter();
            Serializer serializer = saxonProcessor.newSerializer(outputWriter);
            serializer.setOutputProperty(Serializer.Property.METHOD, "text");

            transformer.transform(
                    new StreamSource(new StringReader(xmlPayload)),
                    serializer
            );

            return outputWriter.toString().trim();

        } catch (SaxonApiException e) {
            log.error("XSLT execution error for profile {}: {}", profile, e.getMessage());
            throw new MismoTransformationException("XSLT processing failed: " + e.getMessage(), e);
        }
    }
}
"""

# 9. MismoController.java
controller_java = """package com.example.mismo.controller;

import com.example.mismo.service.MismoProfileDetector;
import com.example.mismo.service.MismoTransformationService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/mismo")
public class MismoController {

    private final MismoTransformationService transformationService;
    private final MismoProfileDetector profileDetector;

    @Value("${mismo.default-profile:mismo-3.4}")
    private String defaultProfile;

    @Value("${mismo.auto-detect-version:true}")
    private boolean autoDetectVersion;

    public MismoController(MismoTransformationService transformationService,
                           MismoProfileDetector profileDetector) {
        this.transformationService = transformationService;
        this.profileDetector = profileDetector;
    }

    @PostMapping(
        value = "/transform",
        consumes = {MediaType.APPLICATION_XML_VALUE, MediaType.TEXT_XML_VALUE},
        produces = MediaType.APPLICATION_JSON_VALUE
    )
    public ResponseEntity<String> transformMismoXml(
            @RequestBody String xmlPayload,
            @RequestHeader(value = "X-MISMO-Profile", required = false) String profileHeader) {

        String profile = profileHeader;
        if (profile == null || profile.isBlank()) {
            if (autoDetectVersion) {
                profile = profileDetector.detectProfile(xmlPayload, defaultProfile);
            } else {
                profile = defaultProfile;
            }
        }

        // 1. Validate XML against profile schema
        transformationService.validateXml(xmlPayload, profile);

        // 2. Transform XML to JSON via XSLT
        String jsonOutput = transformationService.transformToJson(xmlPayload, profile);

        return ResponseEntity.ok(jsonOutput);
    }
}
"""

# 10. Application Entry Point
app_java = """package com.example.mismo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MismoTransformerApplication {
    public static void main(String[] args) {
        SpringApplication.run(MismoTransformerApplication.class, args);
    }
}
"""

# 11. Schemas & Stylesheets
schema_34 = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://www.mismo.org/residential/2009/schemas"
           xmlns="http://www.mismo.org/residential/2009/schemas"
           elementFormDefault="qualified">

    <xs:element name="MESSAGE">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="DEAL_SETS">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="DEAL_SET">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="DEALS">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:element name="DEAL" maxOccurs="unbounded">
                                                        <xs:complexType>
                                                            <xs:sequence>
                                                                <xs:element name="LOANS">
                                                                    <xs:complexType>
                                                                        <xs:sequence>
                                                                            <xs:element name="LOAN" maxOccurs="unbounded">
                                                                                <xs:complexType>
                                                                                    <xs:sequence>
                                                                                        <xs:element name="LOAN_IDENTIFIERS">
                                                                                            <xs:complexType>
                                                                                                <xs:sequence>
                                                                                                    <xs:element name="LOAN_IDENTIFIER" maxOccurs="unbounded">
                                                                                                        <xs:complexType>
                                                                                                            <xs:sequence>
                                                                                                                <xs:element name="LoanIdentifierValue" type="xs:string"/>
                                                                                                            </xs:sequence>
                                                                                                        </xs:complexType>
                                                                                                    </xs:element>
                                                                                                </xs:sequence>
                                                                                            </xs:complexType>
                                                                                        </xs:element>
                                                                                        <xs:element name="TERMS_OF_LOAN">
                                                                                            <xs:complexType>
                                                                                                <xs:sequence>
                                                                                                    <xs:element name="BaseLoanAmount" type="xs:decimal"/>
                                                                                                </xs:sequence>
                                                                                            </xs:complexType>
                                                                                        </xs:element>
                                                                                    </xs:sequence>
                                                                                </xs:complexType>
                                                                            </xs:element>
                                                                        </xs:sequence>
                                                                    </xs:complexType>
                                                                </xs:element>
                                                            </xs:sequence>
                                                        </xs:complexType>
                                                    </xs:element>
                                                </xs:sequence>
                                            </xs:complexType>
                                        </xs:element>
                                    </xs:sequence>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
            <xs:attribute name="MISMOVersionID" type="xs:string" use="required"/>
        </xs:complexType>
    </xs:element>
</xs:schema>
"""

schema_closing = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://www.mismo.org/residential/2009/schemas"
           xmlns="http://www.mismo.org/residential/2009/schemas"
           elementFormDefault="qualified">

    <xs:element name="CLOSING_DOCUMENT">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="CLOSING_INFORMATION">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="ClosingDate" type="xs:date"/>
                            <xs:element name="SettlementAgent" type="xs:string"/>
                            <xs:element name="DisbursementAmount" type="xs:decimal"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
            <xs:attribute name="DocumentType" type="xs:string" use="required"/>
        </xs:complexType>
    </xs:element>
</xs:schema>
"""

xslt_34 = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:m="http://www.mismo.org/residential/2009/schemas">

    <xsl:output method="text" encoding="UTF-8"/>

    <xsl:template match="/">
        {
          "mismoVersion": "<xsl:value-of select="/*/@MISMOVersionID"/>",
          "loans": [
            <xsl:for-each select="//m:LOAN">
              {
                "loanIdentifier": "<xsl:value-of select="m:LOAN_IDENTIFIERS/m:LOAN_IDENTIFIER/m:LoanIdentifierValue"/>",
                "loanAmount": <xsl:value-of select="m:TERMS_OF_LOAN/m:BaseLoanAmount"/>
              }<xsl:if test="position() != last()">,</xsl:if>
            </xsl:for-each>
          ]
        }
    </xsl:template>
</xsl:stylesheet>
"""

xslt_closing = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:m="http://www.mismo.org/residential/2009/schemas">

    <xsl:output method="text" encoding="UTF-8"/>

    <xsl:template match="/">
        {
          "documentType": "<xsl:value-of select="/*/@DocumentType"/>",
          "closingDate": "<xsl:value-of select="//m:CLOSING_INFORMATION/m:ClosingDate"/>",
          "settlementAgent": "<xsl:value-of select="//m:CLOSING_INFORMATION/m:SettlementAgent"/>",
          "disbursementAmount": <xsl:value-of select="//m:CLOSING_INFORMATION/m:DisbursementAmount"/>
        }
    </xsl:template>
</xsl:stylesheet>
"""

# 12. Test Cases
service_test_java = """package com.example.mismo.service;

import com.example.mismo.exception.MismoValidationException;
import com.example.mismo.exception.UnsupportedProfileException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MismoTransformationServiceTest {

    private MismoTransformationService service;

    private final String valid34Xml = \"\"\"
            <MESSAGE xmlns="http://www.mismo.org/residential/2009/schemas" MISMOVersionID="3.4">
                <DEAL_SETS>
                    <DEAL_SET>
                        <DEALS>
                            <DEAL>
                                <LOANS>
                                    <LOAN>
                                        <LOAN_IDENTIFIERS>
                                            <LOAN_IDENTIFIER>
                                                <LoanIdentifierValue>LN-9928172</LoanIdentifierValue>
                                            </LOAN_IDENTIFIER>
                                        </LOAN_IDENTIFIERS>
                                        <TERMS_OF_LOAN>
                                            <BaseLoanAmount>450000.00</BaseLoanAmount>
                                        </TERMS_OF_LOAN>
                                    </LOAN>
                                </LOANS>
                            </DEAL>
                        </DEALS>
                    </DEAL_SET>
                </DEAL_SETS>
            </MESSAGE>
            \"\"\";

    private final String invalid34Xml = \"\"\"
            <MESSAGE xmlns="http://www.mismo.org/residential/2009/schemas" MISMOVersionID="3.4">
                <DEAL_SETS>
                    <DEAL_SET>
                        <!-- Missing required DEALS structure -->
                    </DEAL_SET>
                </DEAL_SETS>
            </MESSAGE>
            \"\"\";

    private final String closingXml = \"\"\"
            <CLOSING_DOCUMENT xmlns="http://www.mismo.org/residential/2009/schemas" DocumentType="ClosingDisclosure">
                <CLOSING_INFORMATION>
                    <ClosingDate>2026-09-15</ClosingDate>
                    <SettlementAgent>First American Title</SettlementAgent>
                    <DisbursementAmount>325000.00</DisbursementAmount>
                </CLOSING_INFORMATION>
            </CLOSING_DOCUMENT>
            \"\"\";

    @BeforeEach
    void setUp() {
        service = new MismoTransformationService();
    }

    @Test
    @DisplayName("Validate valid MISMO 3.4 XML successfully")
    void testValidateXmlSuccess() {
        assertDoesNotThrow(() -> service.validateXml(valid34Xml, "mismo-3.4"));
    }

    @Test
    @DisplayName("Validation fails when schema structure is violated")
    void testValidateXmlFailure() {
        assertThrows(MismoValidationException.class, () -> service.validateXml(invalid34Xml, "mismo-3.4"));
    }

    @Test
    @DisplayName("Validation fails when unknown profile is given")
    void testValidateUnknownProfile() {
        assertThrows(UnsupportedProfileException.class, () -> service.validateXml(valid34Xml, "unknown-profile"));
    }

    @Test
    @DisplayName("Transform valid MISMO 3.4 XML to target JSON format")
    void testTransform34ToJson() {
        String json = service.transformToJson(valid34Xml, "mismo-3.4");
        assertNotNull(json);
        assertTrue(json.contains("\\\"mismoVersion\\\": \\\"3.4\\\""));
        assertTrue(json.contains("\\\"loanIdentifier\\\": \\\"LN-9928172\\\""));
        assertTrue(json.contains("\\\"loanAmount\\\": 450000.00"));
    }

    @Test
    @DisplayName("Transform valid MISMO Closing XML to target JSON format")
    void testTransformClosingToJson() {
        assertDoesNotThrow(() -> service.validateXml(closingXml, "mismo-closing"));
        String json = service.transformToJson(closingXml, "mismo-closing");
        assertNotNull(json);
        assertTrue(json.contains("\\\"documentType\\\": \\\"ClosingDisclosure\\\""));
        assertTrue(json.contains("\\\"settlementAgent\\\": \\\"First American Title\\\""));
        assertTrue(json.contains("\\\"disbursementAmount\\\": 325000.00"));
    }
}
"""

controller_test_java = """package com.example.mismo.controller;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class MismoControllerTest {

    @Autowired
    private MockMvc mockMvc;

    private final String valid34Xml = \"\"\"
            <MESSAGE xmlns="http://www.mismo.org/residential/2009/schemas" MISMOVersionID="3.4">
                <DEAL_SETS>
                    <DEAL_SET>
                        <DEALS>
                            <DEAL>
                                <LOANS>
                                    <LOAN>
                                        <LOAN_IDENTIFIERS>
                                            <LOAN_IDENTIFIER>
                                                <LoanIdentifierValue>LN-9928172</LoanIdentifierValue>
                                            </LOAN_IDENTIFIER>
                                        </LOAN_IDENTIFIERS>
                                        <TERMS_OF_LOAN>
                                            <BaseLoanAmount>450000.00</BaseLoanAmount>
                                        </TERMS_OF_LOAN>
                                    </LOAN>
                                    <LOAN>
                                        <LOAN_IDENTIFIERS>
                                            <LOAN_IDENTIFIER>
                                                <LoanIdentifierValue>LN-9928173</LoanIdentifierValue>
                                            </LOAN_IDENTIFIER>
                                        </LOAN_IDENTIFIERS>
                                        <TERMS_OF_LOAN>
                                            <BaseLoanAmount>125000.50</BaseLoanAmount>
                                        </TERMS_OF_LOAN>
                                    </LOAN>
                                </LOANS>
                            </DEAL>
                        </DEALS>
                    </DEAL_SET>
                </DEAL_SETS>
            </MESSAGE>
            \"\"\";

    private final String invalid34Xml = \"\"\"
            <MESSAGE xmlns="http://www.mismo.org/residential/2009/schemas" MISMOVersionID="3.4">
                <DEAL_SETS>
                    <DEAL_SET>
                        <!-- Incomplete elements -->
                    </DEAL_SET>
                </DEAL_SETS>
            </MESSAGE>
            \"\"\";

    private final String closingXml = \"\"\"
            <CLOSING_DOCUMENT xmlns="http://www.mismo.org/residential/2009/schemas" DocumentType="ClosingDisclosure">
                <CLOSING_INFORMATION>
                    <ClosingDate>2026-09-15</ClosingDate>
                    <SettlementAgent>First American Title</SettlementAgent>
                    <DisbursementAmount>325000.00</DisbursementAmount>
                </CLOSING_INFORMATION>
            </CLOSING_DOCUMENT>
            \"\"\";

    @Test
    @DisplayName("Auto-detects MISMO version from root element attribute when no header is supplied")
    void testAutoDetectionSuccess() throws Exception {
        mockMvc.perform(post("/api/v1/mismo/transform")
                        .contentType(MediaType.APPLICATION_XML)
                        .content(valid34Xml))
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.mismoVersion").value("3.4"))
                .andExpect(jsonPath("$.loans[0].loanIdentifier").value("LN-9928172"))
                .andExpect(jsonPath("$.loans[0].loanAmount").value(450000.00))
                .andExpect(jsonPath("$.loans[1].loanIdentifier").value("LN-9928173"))
                .andExpect(jsonPath("$.loans[1].loanAmount").value(125000.50));
    }

    @Test
    @DisplayName("Explicit header overrides and matches closing document profile")
    void testCustomHeaderSuccess() throws Exception {
        mockMvc.perform(post("/api/v1/mismo/transform")
                        .header("X-MISMO-Profile", "mismo-closing")
                        .contentType(MediaType.APPLICATION_XML)
                        .content(closingXml))
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.documentType").value("ClosingDisclosure"))
                .andExpect(jsonPath("$.settlementAgent").value("First American Title"))
                .andExpect(jsonPath("$.disbursementAmount").value(325000.00));
    }

    @Test
    @DisplayName("Invalid XML triggers structured 400 Bad Request ErrorResponse")
    void testValidationFailureStructuredResponse() throws Exception {
        mockMvc.perform(post("/api/v1/mismo/transform")
                        .header("X-MISMO-Profile", "mismo-3.4")
                        .contentType(MediaType.APPLICATION_XML)
                        .content(invalid34Xml))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("XSD Validation Failed"))
                .andExpect(jsonPath("$.details").exists())
                .andExpect(jsonPath("$.timestamp").exists());
    }

    @Test
    @DisplayName("Unsupported profile returns clean 400 response with message")
    void testUnsupportedProfileResponse() throws Exception {
        mockMvc.perform(post("/api/v1/mismo/transform")
                        .header("X-MISMO-Profile", "non-existent-profile")
                        .contentType(MediaType.APPLICATION_XML)
                        .content(valid34Xml))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Unsupported MISMO Profile"))
                .andExpect(jsonPath("$.details", containsString("not found")));
    }
}
"""

# Sample XML files
sample_valid_34 = """<MESSAGE xmlns="http://www.mismo.org/residential/2009/schemas" MISMOVersionID="3.4">
    <DEAL_SETS>
        <DEAL_SET>
            <DEALS>
                <DEAL>
                    <LOANS>
                        <LOAN>
                            <LOAN_IDENTIFIERS>
                                <LOAN_IDENTIFIER>
                                    <LoanIdentifierValue>LN-9928172</LoanIdentifierValue>
                                </LOAN_IDENTIFIER>
                            </LOAN_IDENTIFIERS>
                            <TERMS_OF_LOAN>
                                <BaseLoanAmount>450000.00</BaseLoanAmount>
                            </TERMS_OF_LOAN>
                        </LOAN>
                    </LOANS>
                </DEAL>
            </DEALS>
        </DEAL_SET>
    </DEAL_SETS>
</MESSAGE>
"""

sample_valid_closing = """<CLOSING_DOCUMENT xmlns="http://www.mismo.org/residential/2009/schemas" DocumentType="ClosingDisclosure">
    <CLOSING_INFORMATION>
        <ClosingDate>2026-09-15</ClosingDate>
        <SettlementAgent>First American Title</SettlementAgent>
        <DisbursementAmount>325000.00</DisbursementAmount>
    </CLOSING_INFORMATION>
</CLOSING_DOCUMENT>
"""

readme_content = """# MISMO XML-to-JSON Spring Boot Microservice

Production-grade Spring Boot 3.2.x microservice built with Java 17 and Saxon-HE 12.4 for validating and transforming diverse MISMO XML payloads into clean JSON documents.

---

## Key Architectural Highlights

1. **Auto-Detection & Profile Routing**:
   - Inspects the XML root element and `MISMOVersionID` attribute using a fast StAX reader (`XMLStreamReader`) to determine whether it is `mismo-3.4`, `mismo-closing`, etc.
   - Allows explicit override via the `X-MISMO-Profile` HTTP request header.
2. **Schema Validation & XXE Protection**:
   - Validates incoming payloads using standard W3C XSD specifications.
   - Full OWASP XXE (XML External Entity) injection protection enabled on both XML Schema Factories and StAX readers.
3. **High Performance Thread-Safe Caching**:
   - `Schema` and Saxon `XsltExecutable` instances are compiled once and stored in `ConcurrentHashMap` caches.
4. **Resilient Error Handling**:
   - `@RestControllerAdvice` translates schema errors, missing profiles, and parsing issues into RFC-compliant JSON `ErrorResponse` objects with timestamps and HTTP status codes.
5. **Actuator & Observability**:
   - Health and metrics endpoints enabled at `/actuator/health`.

---

## Directory Layout"""