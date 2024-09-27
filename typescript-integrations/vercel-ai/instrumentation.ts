import { registerOTel } from '@vercel/otel'
import { ConsoleSpanExporter } from '@opentelemetry/sdk-trace-base'
 
export function register() {
  registerOTel({ serviceName: 'next-app', traceExporter: new ConsoleSpanExporter() })
}