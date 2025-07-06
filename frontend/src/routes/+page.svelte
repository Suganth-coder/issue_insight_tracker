<script lang="ts">
    import {SignedIn, SignedOut} from 'svelte-clerk';
    import {goto} from '$app/navigation';
    import Header from '$lib/components/header.svelte';

    function gotoDashboard(){
        $effect(() => {
        goto('/dashboard');
    })
    }
</script>

<div class="container my-3">
    <Header />

    <SignedIn>
        {gotoDashboard()}
    </SignedIn>
    
    <main class="py-4">
        <SignedOut>
            <div class="card shadow-sm p-4 mb-4 bg-light text-center">
                <div class="card-body">
                    <h2 class="card-title mb-3">Welcome to Issue Insight Tracker</h2>
                    <p class="card-text">Kindly sign in to continue</p>
                </div>
            </div>
        </SignedOut>
        

    </main>

    <footer class="py-3 border-top text-center mt-auto">
        <p class="mb-0">© 2025 Issue Insight Tracker</p>
    </footer>
</div>


<style>
    .card.shadow-sm {
        background: rgba(30, 30, 30, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
        
    .card.shadow-sm:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
    }

    .card-body {
        padding: 2rem !important;
    }
        
    .card-title {
        font-size: 1.75rem !important;
        margin-bottom: 1rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
        
    .card-text {
        font-size: 1.1rem !important;
        color: rgba(255, 255, 255, 0.7) !important;
    }

        
</style>
