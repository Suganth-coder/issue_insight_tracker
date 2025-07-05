<script lang="ts">
	import { SignedIn, SignedOut, SignInButton, UserButton} from 'svelte-clerk';
    import {useClerkContext} from 'svelte-clerk/client';
    // import {goto} from '$app/navigation';

    const context = useClerkContext();
    const fetchData = async () => {
        const token = await context.session?.getToken();
        console.log('Token:', token);
    }
    
    import '$lib/styles/signed.css';
    // $effect(() => {
    //     goto('/dashboard');
    // })

</script>

<!---
What to do:
After successful sign in redirect to the dashboard page
* State Check 
* Redirect tot dashbaord page

Use <SignedIn> to execute code when the user is signed in.

-->

<header>
    
    <SignedOut>
        <SignInButton />
    </SignedOut>
    <SignedIn>
        <!-- Redirect to the dashboard page -->
        <UserButton />
    </SignedIn>
</header>

{fetchData()}
