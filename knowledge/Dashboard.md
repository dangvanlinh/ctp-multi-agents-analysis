# CTP Knowledge Dashboard

## Revenue Overview (T3/2026)

```dataview
TABLE feature AS "Feature", type AS "Type", revenue AS "Rev (M)", share + "%" AS "Share", status AS "Status"
FROM "features"
WHERE feature != null
SORT revenue DESC
```

## Backlog Items (chưa giải quyết)

```dataview
TASK
FROM "features"
WHERE !completed
GROUP BY file.link
```

## Recently Updated

```dataview
TABLE updated AS "Last Updated", join(tags, ", ") AS "Tags"
FROM "features"
WHERE feature != null
SORT updated DESC
```

## Quick Links

- [[features/_index|Feature Map & Cross-Dependencies]]
- [[game-design|Game Design Philosophy]]
- [[economy|Economy Overview]]
- [[player-behavior|Player Behavior]]
- [[analysis-flows|Analysis Frameworks]]
- [[resolved|Quyết định đã CHỐT]]
