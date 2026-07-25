# 승인 시안 충실도 루프

일반 심미성 검증은 현재 화면 자체의 완성도를 봅니다. 승인 시안 충실도 검증은 다른 질문을 다룹니다. 최초에 승인한 방향의 핵심 구성과 작업 흐름이 실제 구현까지 살아 있는지 확인합니다.

두 검증은 서로 대체할 수 없습니다. 현재 화면만 보고 높은 점수를 받아도, 승인 시안의 비대칭 구성·첫 화면 작업 우선순위·문맥 rail·선택 상태 연결이 사라졌다면 이 게이트는 실패해야 합니다.

## 권한 경계

승인 시안이 비교 기준이 될 수 있는 범위는 계약에 명시된 다음 항목뿐입니다.

- composition
- morphology
- density
- hierarchy
- contextual linkage
- task visibility
- responsive translation

색상은 `docs/color-reference.md`에 내장된 Semantic OS graph가 결정합니다. 서체, 정보 구조, 제품 문구, 로고, 재배포 에셋 역시 각각의 저작 산출물이 우선합니다. 승인 이미지와 닮았다는 이유로 이 값을 가져오거나 유사도 점수를 만들면 계약 검증이 실패합니다.

## 산출물

### `reference-fidelity-contract/v1`

`projects/<name>/design-system/reference-fidelity-contract.json`에 둡니다. 다음 내용을 해시로 고정합니다.

- 승인 방향 문서
- 승인 이미지
- 비교를 허용하지 않는 범위
- 보존할 metric과 근거 문장
- metric별 최소 점수와 critical 여부
- 전체 문턱과 최대 반복 횟수

이 계약은 Visual 단계에서 작성하고, Fidelity Auditor는 수정할 수 없습니다.

### `reference-fidelity-review-artifact/v1`

각 리뷰는 승인 이미지와 현재 스크린샷을 한 화면에서 비교한 멀티모달 검토 기록입니다. 계약 SHA, 승인 이미지 SHA, 현재 runtime-tree SHA, 현재 스크린샷 SHA를 함께 보관합니다. 각 metric에는 점수뿐 아니라 구체적인 관찰과 실패 시 수정 지시가 들어가야 합니다.

### `reference-fidelity-loop/v1`

CLI가 리뷰를 다시 계산해 만든 반복 보고서입니다. 같은 스크린샷 SHA 묶음을 재사용한 점수 변경은 다음 반복으로 인정하지 않습니다. 마지막 반복만 출고 상태를 결정합니다.

## 실행 순서

```bash
uv run design-ontology reference-fidelity-loop \
  --project-dir projects/<name> \
  --target-repo <implementation-repo> \
  --contract projects/<name>/design-system/reference-fidelity-contract.json \
  --screenshot-manifest projects/<name>/build/system/production/screenshots.json \
  --review-artifact projects/<name>/build/system/production/reference-fidelity/review-01.json
```

실패하면 보고서의 `next_iteration_brief`만 구현 수정에 사용합니다. 계약이나 승인 이미지를 낮춰서 통과시키면 안 됩니다.

```text
UI Implementer
  → Approved-Reference Fidelity Auditor
      ├─ 실패: 수정 브리프 → UI Implementer → 새 runtime·새 screenshot
      └─ 통과: Production QA → Release Governor
```

`verify-production-ui`는 `design-system/references/selected-direction.md`가 있으면 fidelity contract를 필수로 요구합니다. 계약만 있고 보고서가 없거나, 해시가 오래됐거나, 마지막 paired review가 실패해도 출고가 차단됩니다.
