# presets/.metrics/

수동 입력 카운터. `catalog-health` (Phase 15-1) 와 향후 pruning (Phase 15-4) 의 입력.

- `install_hits.json` — `{preset_id: count}` 형태. `/design-start` 설치 통계 수동 누적.
- `match_hits.json` — `{preset_id: count}` 형태. matcher Top-1 선택 횟수 수동 누적.

자동 수집 파이프라인은 별도 Phase. 파일이 없거나 키가 없으면 0 으로 간주.
