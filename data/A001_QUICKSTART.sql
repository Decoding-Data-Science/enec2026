-- ENEC 2026 / Nuclear Enterprise 360 V2.2
-- Beginner-friendly A-001 starter queries

-- 1. Find A-001
SELECT *
FROM assets
WHERE asset_id = 'A-001';

-- 2. Current 360-degree view
SELECT *
FROM asset_360
WHERE asset_id = 'A-001';

-- 3. Recommended forecasting dataset
SELECT *
FROM a001_sensor_hourly
ORDER BY hour_timestamp
LIMIT 48;

-- 4. A-001 project relationships
SELECT *
FROM asset_project_map
WHERE asset_id = 'A-001'
ORDER BY project_id;

-- 5. Risks connected to A-001 projects
SELECT *
FROM asset_project_risk_map
WHERE asset_id = 'A-001'
ORDER BY project_id, risk_scope DESC, exposure_score DESC;

-- 6. Full A-001 event timeline
SELECT *
FROM a001_event_timeline
ORDER BY event_timestamp;

-- 7. Document evidence links
SELECT *
FROM a001_document_evidence
ORDER BY document_id;

-- 8. Current A-001 source-document metadata
SELECT document_id, title, document_type, approval_status, version, issue_date
FROM a001_source_documents
ORDER BY issue_date;
