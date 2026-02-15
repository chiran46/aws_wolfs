# Requirements Document

## Introduction

CarbonSakthi is an AI-powered carbon credit access bridge that enables small and marginal farmers in India to participate in carbon markets. The platform uses AWS AI services, agentic workflows, and RAG-based reasoning to simplify eligibility assessment, carbon estimation, farmer education, aggregation, and corporate matching. The system addresses the critical gap where small farmers practice sustainable agriculture but lack awareness, understanding, and access to carbon credit opportunities.

## Glossary

- **System**: The CarbonSakthi AI platform
- **Farmer**: Small or marginal farmer with 1-5 acres of land
- **FPO**: Farmer Producer Organization
- **Carbon_Credit**: A tradable certificate representing one metric ton of CO₂ equivalent (tCO₂e) removed or reduced
- **RAG_Pipeline**: Retrieval-Augmented Generation system for document-based reasoning
- **Agentic_Workflow**: Multi-step AI agent orchestration using Amazon Bedrock Agents
- **Eligibility_Engine**: Component that validates farmer practices against carbon methodology standards
- **Estimation_Engine**: Component that calculates potential carbon credits using standardized coefficients
- **Aggregation_Engine**: Component that clusters farmers to meet minimum carbon thresholds
- **Matching_Engine**: Component that connects farmer clusters with corporate demand
- **Voice_Interface**: Speech-to-text and text-to-speech system supporting local Indian languages
- **Corporate_User**: Sustainability officer or ESG team member seeking carbon credits
- **Carbon_Methodology**: Standardized guidelines defining eligible practices and calculation methods
- **Cluster**: Group of farmers aggregated to meet minimum carbon volume requirements
- **tCO₂e**: Metric tons of carbon dioxide equivalent

## Requirements

### Requirement 1: Farmer Data Collection

**User Story:** As a farmer, I want to provide my agricultural information through voice or text, so that the system can assess my eligibility for carbon credits.

#### Acceptance Criteria

1. WHEN a farmer initiates data collection, THE System SHALL collect land size, crop type, irrigation method, fertilizer usage, tillage method, agroforestry presence, and location
2. WHEN a farmer provides input via voice, THE Voice_Interface SHALL transcribe speech to text in the farmer's local language
3. WHEN a farmer provides incomplete data, THE System SHALL prompt for missing required fields
4. WHEN data collection is complete, THE System SHALL store the farmer profile in the database
5. WHEN network connectivity is low, THE System SHALL operate in offline mode and sync data when connectivity is restored

### Requirement 2: Eligibility Assessment

**User Story:** As a farmer, I want to know if my farming practices qualify for carbon credits, so that I can understand my participation potential.

#### Acceptance Criteria

1. WHEN a farmer profile is complete, THE Eligibility_Engine SHALL validate practices against carbon methodology standards retrieved via RAG_Pipeline
2. WHEN eligibility validation occurs, THE System SHALL cross-reference farmer practices with methodology guidelines stored in the knowledge base
3. WHEN a farmer is eligible, THE System SHALL return eligibility status with qualifying practice details
4. WHEN a farmer is ineligible, THE System SHALL return specific reasons and improvement recommendations
5. WHEN eligibility rules are ambiguous, THE RAG_Pipeline SHALL retrieve relevant methodology sections for reasoning

### Requirement 3: Carbon Credit Estimation

**User Story:** As a farmer, I want to know how many carbon credits I can generate annually, so that I can understand potential income.

#### Acceptance Criteria

1. WHEN a farmer is deemed eligible, THE Estimation_Engine SHALL calculate annual carbon credits using standardized emission coefficients
2. WHEN calculating carbon credits, THE System SHALL apply the formula: Carbon Credits = (Land Area × Crop Coefficient × Practice Factor × Soil Factor)
3. WHEN estimation is complete, THE System SHALL return estimated tCO₂e per year
4. WHEN estimation is complete, THE System SHALL project potential annual income based on carbon price estimates
5. WHEN displaying calculations, THE System SHALL show transparent calculation steps and coefficients used

### Requirement 4: Farmer Education and Recommendations

**User Story:** As a farmer, I want to understand carbon credits and receive improvement suggestions in my local language, so that I can make informed decisions.

#### Acceptance Criteria

1. WHEN a farmer requests explanation, THE System SHALL generate local language content explaining carbon credits, eligibility, and income potential
2. WHEN a farmer is ineligible or has low carbon potential, THE System SHALL provide actionable improvement recommendations
3. WHEN generating recommendations, THE Agentic_Workflow SHALL analyze current practices and suggest specific changes to increase carbon credits
4. WHEN delivering content, THE Voice_Interface SHALL convert text to speech in the farmer's preferred local language
5. WHEN a farmer asks questions, THE RAG_Pipeline SHALL retrieve relevant information from methodology documents to answer

### Requirement 5: Farmer Aggregation and Clustering

**User Story:** As a farmer, I want to be grouped with other farmers to meet minimum carbon thresholds, so that I can access opportunities unavailable to individuals.

#### Acceptance Criteria

1. WHEN a farmer completes assessment, THE Aggregation_Engine SHALL assign the farmer to a geographic cluster
2. WHEN forming clusters, THE System SHALL group farmers by location, crop type, and practice similarity
3. WHEN a cluster reaches minimum carbon threshold, THE System SHALL mark the cluster as market-ready
4. WHEN a farmer views cluster status, THE System SHALL display total cluster carbon volume and member count
5. WHEN cluster composition changes, THE System SHALL recalculate aggregate carbon credits

### Requirement 6: Corporate Demand Matching

**User Story:** As a corporate sustainability officer, I want to discover farmer clusters that meet my carbon credit requirements, so that I can support sustainable agriculture and meet ESG goals.

#### Acceptance Criteria

1. WHEN a corporate user specifies requirements, THE Matching_Engine SHALL filter clusters by carbon volume, location, and practice type
2. WHEN displaying matches, THE System SHALL show cluster details including total tCO₂e, farmer count, geographic distribution, and practice types
3. WHEN a corporate user views a cluster, THE System SHALL provide ESG impact metrics and sustainability narratives
4. WHEN a corporate user requests visualization, THE System SHALL display geographic distribution of matched clusters
5. WHEN matching occurs, THE System SHALL rank clusters by relevance to corporate requirements

### Requirement 7: Voice-First Accessibility

**User Story:** As a farmer with limited literacy, I want to interact with the system using voice in my local language, so that I can access carbon credit opportunities without language barriers.

#### Acceptance Criteria

1. WHEN a farmer selects voice mode, THE Voice_Interface SHALL activate speech recognition for the selected local language
2. WHEN the farmer speaks, THE System SHALL transcribe audio using Amazon Transcribe with language-specific models
3. WHEN the system responds, THE Voice_Interface SHALL synthesize speech using Amazon Polly with natural-sounding local language voices
4. WHEN voice recognition fails, THE System SHALL request the farmer to repeat input
5. WHEN voice interaction completes, THE System SHALL provide text transcript for verification

### Requirement 8: Document Processing and Knowledge Base

**User Story:** As a system administrator, I want to ingest carbon methodology documents, so that the system can reason about eligibility and standards.

#### Acceptance Criteria

1. WHEN a methodology document is uploaded, THE System SHALL extract text using Amazon Textract
2. WHEN text is extracted, THE System SHALL generate embeddings using Amazon Titan Embeddings
3. WHEN embeddings are generated, THE System SHALL store vectors in the vector database for retrieval
4. WHEN the RAG_Pipeline queries the knowledge base, THE System SHALL retrieve the most relevant document sections based on semantic similarity
5. WHEN retrieved content is used, THE System SHALL cite source documents and page numbers

### Requirement 9: Agentic Workflow Orchestration

**User Story:** As a system architect, I want the platform to orchestrate multi-step AI workflows, so that farmer assessment follows a logical, automated process.

#### Acceptance Criteria

1. WHEN a farmer assessment begins, THE Agentic_Workflow SHALL execute steps in sequence: collect inputs, validate eligibility, cross-reference standards, estimate carbon, suggest improvements, assign to cluster
2. WHEN a workflow step fails, THE System SHALL log the error and provide fallback responses
3. WHEN a workflow step requires external data, THE Agentic_Workflow SHALL invoke the appropriate AWS service or database query
4. WHEN a workflow completes, THE System SHALL store the complete assessment result
5. WHEN workflow state needs persistence, THE System SHALL save intermediate results for resumption

### Requirement 10: Low-Bandwidth Operation

**User Story:** As a farmer in a rural area with poor connectivity, I want the system to work with limited internet access, so that I can complete assessments despite network constraints.

#### Acceptance Criteria

1. WHEN network bandwidth is below threshold, THE System SHALL switch to low-bandwidth mode
2. WHEN in low-bandwidth mode, THE System SHALL compress data payloads and reduce media quality
3. WHEN in low-bandwidth mode, THE System SHALL cache frequently accessed content locally
4. WHEN connectivity is lost, THE System SHALL queue operations for later synchronization
5. WHEN connectivity is restored, THE System SHALL sync queued data with the backend

### Requirement 11: Data Security and Privacy

**User Story:** As a farmer, I want my personal and agricultural data to be secure, so that I can trust the platform with sensitive information.

#### Acceptance Criteria

1. WHEN a farmer creates an account, THE System SHALL authenticate users via Amazon Cognito
2. WHEN data is transmitted, THE System SHALL encrypt all communications using TLS
3. WHEN data is stored, THE System SHALL encrypt farmer profiles and assessment results at rest
4. WHEN a user accesses data, THE System SHALL enforce role-based access control via AWS IAM
5. WHEN a farmer requests data deletion, THE System SHALL remove all personal information within 30 days

### Requirement 12: Carbon Estimation Transparency

**User Story:** As a farmer, I want to understand how my carbon credits are calculated, so that I can trust the estimation and identify improvement areas.

#### Acceptance Criteria

1. WHEN displaying carbon estimates, THE System SHALL show the complete calculation formula
2. WHEN displaying carbon estimates, THE System SHALL list all coefficients and factors used with their sources
3. WHEN a farmer questions a calculation, THE System SHALL provide detailed breakdowns by practice type
4. WHEN coefficients are updated, THE System SHALL maintain version history and allow recalculation
5. WHEN estimation methodology changes, THE System SHALL notify affected farmers

### Requirement 13: ESG Reporting for Corporates

**User Story:** As a corporate sustainability officer, I want to generate ESG impact reports from farmer partnerships, so that I can demonstrate environmental and social impact.

#### Acceptance Criteria

1. WHEN a corporate user requests a report, THE System SHALL generate metrics including total tCO₂e offset, number of farmers supported, and geographic reach
2. WHEN generating reports, THE System SHALL include sustainability narratives describing agricultural practices
3. WHEN displaying impact, THE System SHALL visualize carbon reduction over time
4. WHEN a corporate user exports data, THE System SHALL provide reports in standard formats (PDF, CSV)
5. WHEN calculating impact, THE System SHALL aggregate data across all matched clusters

### Requirement 14: System Scalability and Performance

**User Story:** As a system administrator, I want the platform to handle growing user loads efficiently, so that performance remains consistent as adoption increases.

#### Acceptance Criteria

1. WHEN user load increases, THE System SHALL scale compute resources automatically using AWS App Runner or ECS
2. WHEN database queries increase, THE System SHALL maintain response times under 2 seconds for eligibility checks
3. WHEN concurrent voice requests occur, THE System SHALL process them in parallel without degradation
4. WHEN storage grows, THE System SHALL partition data by region and time period
5. WHEN system health degrades, THE System SHALL trigger alerts and auto-recovery procedures

### Requirement 15: Simulation and Demo Mode

**User Story:** As a hackathon participant, I want to demonstrate the platform with simulated data, so that I can showcase functionality without real-world integrations.

#### Acceptance Criteria

1. WHEN demo mode is enabled, THE System SHALL use pre-loaded sample farmer profiles and methodology documents
2. WHEN in demo mode, THE System SHALL simulate carbon price data and corporate demand
3. WHEN demonstrating matching, THE System SHALL show realistic cluster formations and corporate matches
4. WHEN in demo mode, THE System SHALL clearly indicate that no real carbon certification or financial transactions occur
5. WHEN switching between demo and production modes, THE System SHALL maintain separate data stores
