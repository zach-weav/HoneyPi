# HoneyPi Test Plan

## Test Plan Identifier:

Each test case provided will be labeled as "HPI-TC01", "HPI-TC02", etc. Using this labeling convention will
allow for easy location between both this test case document, and the Excel document that will be
used for test case execution.

## Introduction:
 
The purpose of this test plan is to ensure the functionality, reliability, and security of the 
HoneyPi device, a portable intrusion detection system designed to emulate decoy services and collect 
valuable data on potential cyberattacks. Testing the device is critical to validating its capabilities, 
identifying vulnerabilities, and ensuring it meets the intended objectives as an educational tool for 
analyzing common cyberattack techniques. This test plan outlines the approaches and methodologies that 
will be used to verify the effectiveness of the HoneyPi system under various conditions and use cases.

The HoneyPi device will undergo three primary types of testing: ad hoc testing, unit testing, and crowdsourced 
testing. __Ad hoc__ testing will be conducted during the configuration and development phase to provide immediate 
feedback on the system’s performance. These tests will allow for rapid identification of bugs and design flaws, 
ensuring the iterative development process is efficient. __Unit testing__ will follow a more structured approach, 
focusing on individual components of the device, such as container orchestration, honeypot logging mechanisms, 
and network interactions. These tests will be documented in an Excel spreadsheet, specifying test cases, expected results, 
and any deviations observed. Finally, __crowdsourced__ testing will involve peers and collaborators who will use a predefined
test plan and survey to evaluate the device in real-world scenarios. This phase will collect valuable external feedback, 
offering diverse perspectives on the device's usability, functionality, and overall design.

Several constraints may impact the testing procedures. The HoneyPi device relies on the availability of local network environments, 
meaning some tests may be limited by variations in network configurations or restrictions imposed by firewalls and routing policies. 
Additionally, the Raspberry Pi hardware may introduce resource limitations, such as restricted processing power or memory, which could 
affect the performance of the decoy services under high activity. Testers must also adhere to ethical and legal guidelines, ensuring that 
the device is only tested on authorized networks and systems with explicit permission. Despite these constraints, the test plan aims to 
provide a comprehensive assessment of the HoneyPi device’s capabilities while maintaining compliance with ethical standards.

## References:

Link for the project repository: <https://github.com/zachWeav/HoneyPi/tree/master>

Proposal Document: <https://github.com/zachWeav/HoneyPi/blob/master/docs/CSCI497_ProjectProposal_ZachWeaver.pdf>

Requirements document: <https://github.com/zachWeav/HoneyPi/blob/master/docs/CSCI497_ProjectRequirements_ZachWeaver.pdf>


## Test Items:

-   HoneyPi Device

## Device Features to be Tested:

-   Scanning Device for open ports.

-   Decoy Service Availability

-   Decoy SSH server connection.

-   Decoy SQL Database connection.

-   Container Remote Command Execution.

-   Container Intrusion Logging Mechanisms.

-   Container Orchestration Monitoring & Metrics Reporting.

-   Raspberry Pi Host Security

## Features Not to be Tested:

-  Specific Raspberry Pi Device Configuration

-  Advanced Threat Analysis

-  Compatibility Across All Network Environments

-  Device Hardware Resilience

-  Integration with Other Security Mechanisms

## Approach:

Testing the HoenyPi will begin with smaller tests being executed as each docker container is being
configured.  Once all containers are fully built and running emulated services, soft-tests involving individual test
cases will be executed to ensure the device meets all requirements in the project requirements document.  Upon successfully
passing all test cases found in the test case excel document, I will select multiple peers to test the connectivity of each
emulated service and provide valuable feedback and recommendations through a google form.  Any final developments and security
checks will be then be completed before the device is packaged for final deployment.


## Item Pass/Fail Criteria:

Whether or not a test case passes or fails will be determined by a defined
set of questions including:

-   Is the feature of the device functional?

-   Does specific functionality perform as expected?

-   Are there any errors when executing the tests?

-   Was the test sufficient?

If anything still needs to be addressed after executing a test case, 
then the test case is a failure. The device must be fixed and
the feature tested again asking the same questions. If all required criteria are met
with no additional issues found, then the test will be considered a pass.

## HoneyPi Test Cases:

All test cases that will be used in unit testing can be found in the provided excel document:
<https://github.com/zachWeav/HoneyPi/blob/master/tests/HoneyPi_TestCases.xls>

## Test Deliverables:

-   HoneyPi Test Plan

-   HoneyPi Test Cases (excel)

## Test Environment:

The testing environment will primarily involve scanning and connecting to the physical HoneyPi device
from an external machine.  While most tests will be conducted by connecting to the Raspberry Pi via SSH,
I will allow each selected tester to connect to the HoneyPi from their own prefered machine.  Crowdsourced tests will
be conducted under close supervision to ensure all procedures are conducted properly as outlined in the test
cases.

## Estimate:

There are no monetary costs involved for the development or testing of the
device and every tool being used is open sourced and available for public use.

## Schedule:

Testing milestones:

-   Test Plan Completed: __12/9/2024__

-   Ad Hoc Testing: __12/30/2024__

-   Unit-Testing: __1/13/25 - 1/24/25__

-   Crowdsourced Testing: __1/27/25 - 2/07/25__

-   Analyzing Testing Feedback: __2/14/25__

-   Error Fixing: __2/28/25__

-   Applying Device Updates: __3/28/25__

-   Official Testing Report: __4/11/25__

## Responsibilities:

Project Developer (myself):

-   As the project developer, I will be conducting all testing procedures
    to be completed by myself and fellow students.  Furthermore, I will be responsible for
    creating all required documentation, and applying any updated functionality to the
    device.
  
## Risks:

-   __Device Misconfiguration:__ Errors in configuring the decoy services, network settings, or
      logging mechanisms might lead to inaccurate results or failure to capture critical data.

-  __System Security:__ The HoneyPi device is intentionally designed to attract potential attackers.
     If not isolated properly, it might inadvertently expose the network or other devices to potential vulnerabilities.

-  __Inconsistent Testing Environments:__ Ad hoc and crowdsourced testing may introduce inconsistent network conditions
     or varying technical expertise, leading to uneven testing results.

-  __Resource Constraints:__ The HoneyPi hardware may be insufficient to handle extensive testing, such as simultaneous
     attacks or high traffic volumes.


## Assumptions and Dependencies:

>   Device Testing Assumptions:

-  Excluding myself, I will have 5-8 testers

-  Each tester will provide valuable feedback

-  Each tester will have the technical knowlege required

-  Device configuration stability

-  Logging and monitoring functionality

>   Device Testing Dependancies:

-  Hardware and Networking

-  Docker and Docker Compose are configured and running properly

-  Cronjobs are setup to automatically run each container upon system startup

-  NMAP is installed and available to conduct network scans

-  External client can connect to SSH and mySQL container services

-  Project Requirements Documentaion

## Crowd Source Testing Format:

-  __Step-by-step testing instructions:__ TBD

-  __Feedback Form:__ <https://docs.google.com/forms/d/e/1FAIpQLSfeIDc22Gxbko1440cgwGY_AZ2WgMote0zGgy7HYkfzSei_4A/viewform?usp=dialog>


