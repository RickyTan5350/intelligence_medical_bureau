document.addEventListener('DOMContentLoaded', () => {
    const dispatchBtn = document.getElementById('dispatchBtn');
    const queryInput = document.getElementById('queryInput');
    const statusArea = document.getElementById('statusArea');
    const statusSteps = document.querySelectorAll('.status-step');
    const btnText = document.querySelector('.btn-text');
    const loaderRing = document.querySelector('.loader-ring');
    const reportContainer = document.getElementById('reportContainer');
    const reportContent = document.getElementById('reportContent');

    // Simulate animated status progression since backend is synchronous
    function simulateProgress() {
        let currentStep = 0;
        
        statusSteps.forEach(step => {
            step.classList.remove('active', 'done');
        });
        statusSteps[0].classList.add('active');
        statusArea.classList.remove('hidden');

        const interval = setInterval(() => {
            if (currentStep < statusSteps.length - 1) {
                statusSteps[currentStep].classList.remove('active');
                statusSteps[currentStep].classList.add('done');
                currentStep++;
                statusSteps[currentStep].classList.add('active');
            } else {
                clearInterval(interval);
            }
        }, 8000); // Progress every 8 seconds visually

        return interval;
    }

    dispatchBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        if (!query) return;

        // UI State: Loading
        dispatchBtn.disabled = true;
        btnText.textContent = "Swarm Deployed...";
        loaderRing.classList.remove('hidden');
        reportContainer.classList.add('hidden');
        
        const progressInterval = simulateProgress();

        try {
            const response = await fetch('/api/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            clearInterval(progressInterval);

            // Finalize status
            statusSteps.forEach(step => {
                step.classList.remove('active');
                step.classList.add('done');
            });

            if (data.status === 'success') {
                reportContent.innerHTML = marked.parse(data.report);
                reportContainer.classList.remove('hidden');
                
                // Scroll to report
                reportContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                reportContent.innerHTML = `<p style="color: #ef4444;">Error: ${data.message}</p>`;
                reportContainer.classList.remove('hidden');
            }

        } catch (error) {
            clearInterval(progressInterval);
            reportContent.innerHTML = `<p style="color: #ef4444;">Connection Error: ${error.message}</p>`;
            reportContainer.classList.remove('hidden');
        } finally {
            // Restore button state
            setTimeout(() => {
                dispatchBtn.disabled = false;
                btnText.textContent = "Dispatch Swarm";
                loaderRing.classList.add('hidden');
            }, 500);
        }
    });

    // Enter key support
    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            dispatchBtn.click();
        }
    });
});
