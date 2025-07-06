<script>
    import { SignedIn, SignedOut, SignInButton, UserButton} from 'svelte-clerk';

</script>
<div class="container my-3">
    <header class="d-flex justify-content-between align-items-center py-3 border-bottom mb-4">
        <div class="logo">
            <h1 class="h3 mb-0">Issue Insight Tracker</h1>
        </div>
        <div>
            <SignedOut>
                <SignInButton />
            </SignedOut>
            <SignedIn>
                <UserButton />
            </SignedIn>
        </div>
    </header>
</div>

