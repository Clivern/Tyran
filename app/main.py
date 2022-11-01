# MIT License
#
# Copyright (c) 2024 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from fastapi import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.configs import configs
from app.api.router import router
from app.core import models
from app.core.database import engine, wait_for_db
from app.core.logger import get_logger
from app.core.qdrant import get_qdrant
from app.core.middleware import setup_middleware
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


log = get_logger()

log.info("Attempt to migrate the database")

wait_for_db(engine, 30)

models.Base.metadata.create_all(bind=engine)

log.info("Database is migrated")

log.info("Start the app server")

if configs.enable_otlp and not os.getenv("TEST_RUN"):
    log.info("Set up OpenTelemetry Tracer Provider")

    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    log.info("Set up OTLP exporter for traces")

    otlp_exporter = OTLPSpanExporter(
        endpoint=configs.otlp_endpoint, insecure=not configs.secure_otlp
    )
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

app = FastAPI(title=configs.app_name, description=configs.app_description)

if configs.enable_otlp and not os.getenv("TEST_RUN"):
    log.info("Setup FastAPI instrumentor")

    FastAPIInstrumentor.instrument_app(app)

if configs.vector_search_driver == "qdrant" and not os.getenv("TEST_RUN"):
    log.info("Create qdrant collection")
    qdrant_client = get_qdrant()
    qdrant_client.create_collection_if_not_exist(configs.qdrant_db_collection)
    log.info(f"Qdrant collection with name {configs.qdrant_db_collection} got created")

app.include_router(router)

setup_middleware(app)
