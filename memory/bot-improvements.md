# Bot Improvements — Knowledge Transfer from Claude Code

**Fecha:** 2026-04-01
**Fuente:** Análisis de arquitectura de Claude Code (`memory/claude-code-analysis.md`)
**Aplicado a:** Hermes Agent, SecurityBot, QA Bot

---

## Resumen de Cambios

### Hermes Agent (AGENTS.md)
- ✅ Patrones de sistema de tools con Permission Levels
- ✅ Deferred tool loading para tools pesadas
- ✅ ToolContext para estado compartido
- ✅ Cost tracking por sesión (tokens + USD)
- ✅ Auto-compact de contexto cuando se acerca al límite
- ✅ ConversationSession persistence (JSON)
- ✅ Coordinator pattern para multi-agent
- ✅ Task lifecycle con estados definidos
- ✅ Read-before-write enforcement con cache de mtime
- ✅ Feature flags compilados

### SecurityBot (SOUL.md)
- ✅ Sistema de permisos granular (None/ReadOnly/Write/Execute/Dangerous)
- ✅ SecurityPermissionHandler con audit logging
- ✅ Read-before-write enforcement para configs
- ✅ Tool security audit checklist
- ✅ SecurityCostTracker para scans
- ✅ Incident response con three-gate escalation
- ✅ Dependency auditing con CVE tracking
- ✅ Never-panic en tools de seguridad
- ✅ MessageSecurityFilter anti-exfiltración
- ✅ Feature flags de seguridad

### QA Bot (AGENTS.md)
- ✅ Test discovery con deferred loading
- ✅ TestOutcome estructurado (passed/failed/skipped/error)
- ✅ Auto-compact de resultados extensos
- ✅ Permission levels para tests
- ✅ Read-before-write en test fixtures
- ✅ TestCostTracker con estimación de costo
- ✅ Mock-friendly test design con deps injection
- ✅ Temporary directory para tests de archivos
- ✅ Token budget por test
- ✅ Three-gate trigger para scheduling
- ✅ Never-panic en test execution

---

## Patrones Clave Transferidos

### 1. Tool Trait con Permission Levels (Rust → Python)

Claude Code define:
```rust
pub trait Tool {
    fn permission_level(&self) -> PermissionLevel;
    async fn execute(&self, input: Value, ctx: &ToolContext) -> ToolResult;
}
```

Adaptado para Hermes:
```python
registry.register(
    name="file_write",
    permission_level="write",
    is_destructive=False,
)
```

### 2. Three-Gate Triggers (AutoDream → TestScheduler)

Claude Code:
```
Gate 1: TIME → 24 horas
Gate 2: SESSION → 5+ sesiones
Gate 3: LOCK → No otro proceso
```

Adaptado para QA:
```
Gate 1: TIME → 24 horas
Gate 2: SESSION → 5+ news
Gate 3: LOCK → No test en curso
```

### 3. Coordinator Mode (Multi-Agent)

Claude Code define tools internas que solo el coordinator puede usar:
```rust
const INTERNAL_COORDINATOR_TOOLS = &["Agent", "SendMessage", "TaskStop"];
```

Adaptado: `INTERNAL_COORDINATOR_TOOLS = frozenset(["delegate", "send_message", ...])`

### 4. Auto-Compact

Claude Code comprime cuando `tokens > 90% * limit`:
```rust
pub const AUTOCOMPACT_TRIGGER_FRACTION: f64 = 0.90;
pub const KEEP_RECENT_MESSAGES: usize = 10;
```

Adaptado con mismo threshold para mensajes de test results.

### 5. Read-Before-Write Enforcement

Claude Code verifica mtime antes de editar:
```rust
// FileEditTool verifica archivo existe en readFileState cache
```

Adaptado para tests y security: cache de reads con verificación de mtime.

### 6. Never Panic

Todas las tools en Claude Code capturan errores y retornan `ToolResult::error()`. Nunca hacen panic.

Adaptado para QA y Security: try/catch global, `TestOutcome.error()` / `SecurityResult.error()`.

---

## Archivos Modificados

| Archivo | Líneas Añadidas | Tipo |
|---------|----------------|------|
| `/home/jarvis/dept-dev/hermes-agent/AGENTS.md` | ~200 | Patrones de tools, session, coordination |
| `/home/jarvis/dept-dev/ciberseguridad/SOUL.md` | ~150 | Security hardening patterns |
| `/home/jarvis/dept-dev/qa-bot/AGENTS.md` | ~200 | Testing patterns |

---

## Próximos Pasos Recomendados

1. **Implementar CostTracker** en hermes_state.py para tracking real de costos
2. **Agregar SOUL.md** a hermes-agent (no existe actualmente)
3. **Implementar ACP adapter** de hermes-agent (mencionado en estructura, no revisado)
4. **Crear AGENTS.md** para SecurityBot (solo tiene SOUL.md)
5. **Implementar TestScheduler** con three-gate triggers en QA Bot
6. **Integrar ReadStateCache** en tools de archivo de Hermes

---

*Transferido por subagent: 2026-04-01*
