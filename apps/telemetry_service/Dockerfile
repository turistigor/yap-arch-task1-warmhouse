FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as tm_builder

WORKDIR /opt/telemetry/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen


FROM python:3.12-slim

WORKDIR /opt/telemetry/
COPY --from=tm_builder /opt/telemetry/.venv/ .venv/
COPY telemetry/ ./telemetry

ENV PATH="/opt/telemetry/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

ENV PORT=8082
ENV HOST=0.0.0.0

EXPOSE 8082
RUN echo $(ls -la /opt/telemetry/)
CMD python3 -m telemetry
