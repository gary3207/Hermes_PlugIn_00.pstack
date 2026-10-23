# Hermes_PlugIn_pstack

Hermes용 **PStack 플러그인 + 선별 스킬셋**입니다. Lauren Tan의 pstack에서 엔지니어링 판단 기준과 작업 절차를 가져오고, 범위 확대·무확인 자율권·자동 원격 변경·불필요한 필수 절차는 대체했습니다.

**Ponytail과 현재 사용자의 Ground Rule을 대체하지 않습니다.** 짧은 핵심 정책은 자동 제공하고, 16개 작업별 스킬은 필요할 때 선택합니다. 모델·MCP·별도 Python 패키지·Bun·Node·서버·스케줄러를 추가하지 않습니다.

## 새 Hermes에 설치

실행 위치는 Hermes가 설치된 PC의 터미널입니다. 활성 프로필에만 설치합니다.

```text
hermes plugins install gary3207/Hermes_PlugIn_pstack/source/pstack --enable
hermes pstack status
hermes pstack skills
```

설치 후 **새 대화/프로세스**에서 시작하세요. 이미 실행 중인 Desktop·Gateway를 이 플러그인이 자동 종료하거나 재시작하지 않습니다. 스킬 목록이 보인다는 사실과 이미 실행 중인 프로세스가 훅을 로드했다는 사실은 다릅니다.

첫 명령은 GitHub의 `source/pstack`을 네이티브 플러그인으로 설치·활성화합니다. 기본 설정은 `enabled: true`이므로 매번 `/pstack`을 입력할 필요가 없습니다. `status`는 실행 코드의 설정을 확인하는 명령이고 LLM을 호출하지 않습니다.

최신 소스가 아니라 검증된 특정 버전을 복원하려면 공개 커밋의 **40자리 SHA**를 지정합니다.

```text
hermes plugins install gary3207/Hermes_PlugIn_pstack/source/pstack --ref <40-character-commit-sha> --enable
```

`<40-character-commit-sha>`는 실제 커밋 값으로 바꿉니다. 저장소의 기본 분기는 이동할 수 있으며, 고정 커밋 설치는 그 버전의 코드·스킬을 재현합니다. 설치 대상에 동명 플러그인이 있으면 출처와 변경을 먼저 확인하고, `--force`로 무조건 덮어쓰지 마세요.

## 설정·끄기·다시 켜기

```text
hermes pstack status
hermes pstack off
hermes pstack on
```

대화 내 제어 명령은 다음과 같습니다.

```text
/pstack
/pstack status
/pstack off
/pstack on
/pstack skills
```

- `on`/`off`는 **현재 프로필**의 `plugins.entries.pstack.settings.enabled` 불리언만 저장합니다.
- 기본값은 `true`입니다. 설치 직후 별도 설정이 필요 없습니다.
- `off`는 자동 지침 제공만 끕니다. 명시적으로 요청한 스킬은 남아 있습니다. 플러그인 자체를 비활성화하려면 `hermes plugins disable pstack`을 사용하세요.
- 새 PC에서 예전처럼 끄려면 설치 후 `hermes pstack off`를 한 번 실행합니다. 이것이 이 플러그인의 전체 사용자 설정입니다.
- 다른 Profile은 자동 설치·변경하지 않습니다. 필요한 Profile로 전환한 뒤 그곳에서 같은 설치 명령을 사용하세요.

이 설치는 **PStack 패키지와 그 설정**을 재현합니다. 기존 Ponytail 설치, 개인 메모리·Ground Rule 파일·Obsidian 데이터·인증·MCP·JOB·모델 계정은 백업하거나 복원하지 않습니다. 해당 자료와 인증을 저장소에 넣지 마세요.

## 무엇이 자동이고 무엇이 선택인가

플러그인은 Hermes의 `pre_llm_call` 훅으로 [핵심 정책](source/pstack/policy.md)을 제공합니다. 바뀌지 않은 지침은 대화 이력에 매번 중복 추가하지 않고, 압축으로 사라지거나 on/off가 바뀌면 필요한 컨텍스트를 제공합니다. 과거 메시지·시스템 프롬프트·도구 정의를 직접 수정하지 않습니다.

자동 정책은 현재 사용자 권한·안전·Ground Rule 우선, 충분한 직접 근거, 재사용·비례 검증, 사용자 변경 보존, `source/`와 산출물 위치, 프로필 경계, 실제 다단계 진행 보고를 다룹니다.

**이는 모델에 제공하는 작업 지침이지, 권한 차단기나 코드 품질 보증 장치가 아닙니다.** 기존 Hermes 승인·보안 검사를 대체하거나 우회하지 않습니다. 훅 테스트 통과는 실제 모든 대화에서 모델이 지침을 준수한다는 보장이 아닙니다.

자연어로 작업을 요청하면 필요에 맞는 스킬을 선택하도록 안내합니다. 확실히 지정하고 싶다면 다음처럼 요청할 수 있습니다.

```text
pstack:impact 스킬로 이 변경의 영향과 미확인 계약을 검토해줘. 수정은 하지 마.
pstack:diagnose 스킬로 이 오류의 원인을 조사해줘.
pstack:reliability 스킬로 재시도·취소·중복 실행 위험을 확인해줘.
```

에이전트는 `skill_view(name='pstack:impact')` 같은 네이티브 스킬 조회를 사용합니다. 16개 스킬을 전부 읽거나 별도 플래닝 절차를 항상 실행하지 않습니다.

| 스킬 | 목적 |
|---|---|
| `pstack:evidence` | 동작·의도·사실·추론·가설·미확인 구분 |
| `pstack:diagnose` | 재현·전제 반증·근본 원인·회귀 확인 |
| `pstack:impact` | 호출자·외부 데이터·동적 생명주기 영향 |
| `pstack:design` | 도메인 구조·소유권·설계 위험 신호 |
| `pstack:reliability` | 재시도 수렴·취소·공유 쓰기 보호 |
| `pstack:review` | 독립 리뷰 결과의 수정·고려·참고·기각 |
| `pstack:verify` | 실제 사용자 경로·증거 보존·검증 drift |
| `pstack:measure` | 공정한 성능 비교·오측정·개선 루프 |
| `pstack:evaluate` | Prompt·스킬 후보의 제한된 실제 비교 |
| `pstack:handoff` | 중단·재개·현재 상태·결정 근거 |
| `pstack:learn` | 반복 실수와 검증 교훈의 최소 예방 조치 |
| `pstack:explain` | 독자 수준에 맞춘 설명·기술 문서 |
| `pstack:formal` | 구체적 상태·동시성 속성의 범위 제한 검증 |
| `pstack:work` | 승인된 기능·리팩터링·단계별 검증 |
| `pstack:compare` | 필요한 대안 비교·독립 병렬 작업 |
| `pstack:git` | 승인된 PR 조회·대응·발행·병합의 경계 |

## 교체한 운영 규칙

| 가져오지 않은 원문 기본값 | 이 패키지의 대체 규칙 |
|---|---|
| 가역적이면 먼저 하고 사후 교정 | 승인 범위 안에서 진행; 실제 범위·목적·위험 모호함은 확인 |
| 모든 증거 범주·전체 과거 조사 | 관련 직접 근거 우선, 답이 충분하면 종료 |
| 함수 경계마다 복수 설계·고정 10 lane | 실제 위험·불확실성·비용에 비례해 선택 |
| 발견한 문제 즉시 수정·외부 backlog 등록 | 범위 밖 발견은 근거와 함께 제안 |
| 자동 push·reset·rebase·삭제 | 명시 승인 범위·사용자 변경 보존·실제 대상 read-back |
| 모호한 제약 주석 삭제·내부 무조건 신뢰 | 필요한 안전 제약·런타임 불변식 보존 |
| 별도 전역 작업 원장·대화 채굴 | 기존 기록 체계를 우선하고 필요한 자료만 조회 |
| 영어 문체·금지 문장부호·고정 그림 수 | 사용자 언어·독자 수준·문서 목적에 맞춤 |

[전체 80개 항목의 채택·대체·제외 근거](source/docs/SELECTION.md)와 [출처·라이선스 안내](source/pstack/NOTICE.md)를 확인할 수 있습니다. 고가의 기법을 금지하지는 않지만 일반 작업의 새 필수 게이트로 만들지 않습니다.

## 검증·개발

Python의 표준 라이브러리만으로 오프라인 회귀 검사를 실행합니다. 실행 위치는 이 저장소 루트입니다.

```text
python -m unittest discover -s source/tests -p test_pstack.py -v
hermes plugins validate source/pstack --json
hermes plugins doctor source/pstack --ci
```

테스트는 컨텍스트 중복 방지, 압축 이후 재주입, 멀티모달 이력, on/off 전환, 설정 격리, 읽기 전용 상태 조회, 실제 스킬 파일과 메타데이터를 확인합니다. 네이티브 설치 검증은 별도 임시 `HERMES_HOME`에서 수행하며 실제 인증·메모리·JOB을 복사하지 않습니다.

현재 검증 기준은 Hermes `0.22.4`, Python `3.14.7`, Windows입니다. 실행 코드는 `pathlib`·JSON 등 표준 라이브러리와 네이티브 PluginContext API만 사용하지만, 다른 OS에서의 실사용·새 OS 설치·모든 LLM의 동작을 검증했다고 주장하지 않습니다.

## 범위와 비목표

- Hermes Core·Desktop·Gateway 소스 변경 없음.
- 새 도구·모델 호출·외부 메시지·서버·cron·JOB·네트워크 노출 없음.
- 기존 Ponytail·관리형 정책·다른 플러그인·다른 Profile 변경 없음.
- 원본 Cursor `poteto-mode`의 전체 실행기나 도구를 그대로 이식한 패키지가 아님.
- TLA+/TLC·Bun·Cursor Automations·Benny·Grok Bot을 설치하지 않음. 관련 기법은 실제 요청과 가용 도구에 맞는 절차만 보존.

## 출처와 라이선스

pstack by Lauren Tan의 MIT 라이선스 자료를 선별·재작성한 독립적인 Hermes 어댑테이션입니다. Cursor·Nous Research의 공식 배포물이 아닙니다. upstream 기준은 `gary3207/plugins`의 `pstack/`, 커밋 `8b3326d99fd4b993cb33a24dad8af03175c642c5`, manifest `0.15.30`입니다.

[MIT 라이선스](LICENSE). upstream의 저작권·허가 문구를 설치 패키지에도 포함합니다.
