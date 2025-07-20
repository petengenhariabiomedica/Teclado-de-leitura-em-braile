document.addEventListener("DOMContentLoaded", () => {
    const output = document.getElementById("output");
    const status = document.getElementById("status");
    const progressBar = document.getElementById("progress-bar");

    if (output && status) {
        const eventSource = new EventSource("/stream");

        let charCount = 0;
        const estimatedTotal = 5000; // valor estimado, pode ser ajustado

        status.textContent = "⏳ Iniciando transmissão...";
        output.textContent = "";

        eventSource.onmessage = (event) => {
            const data = event.data;

            if (data === "done") {
                status.textContent = "✅ Envio concluído!";
                if (progressBar) progressBar.value = 100;
                eventSource.close();
            } else {
                charCount += 1;
                output.textContent += data;
                output.scrollTop = output.scrollHeight;

                status.textContent = `✉️ Enviando caracteres... (${charCount})`;

                if (progressBar) {
                    let percent = Math.min((charCount / estimatedTotal) * 100, 100);
                    progressBar.value = percent;
                }
            }
        };

        eventSource.onerror = () => {
            status.textContent = "❌ Erro na comunicação com o servidor.";
            eventSource.close();
        };
    }
});

