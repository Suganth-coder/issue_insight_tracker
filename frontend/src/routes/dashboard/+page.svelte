<script>
    import {addAttachmentAPI, addIssueAPI} from '$lib/issues/issueManagement';
    import {useClerkContext} from 'svelte-clerk/client';

    let issues = [];
    let showAddIssuediv = false;
    let filename = null;

    let issueTitle = '';
    let issueDescription = '';

    function addIssueDIV(){
        showAddIssuediv = true;
    }

    const context = useClerkContext();
    let get_token = async () => {
        return await context.session?.getToken();
    };

    let addAttachment = async(file) => {
        if (!file) return;
        const token = await get_token();
        let result = await addAttachmentAPI(file, token);

        if (result != 500) {
            filename = result;
        }
    }

    let addIssue = async() => {

        const token = await get_token();

        let data = {
            title: issueTitle,
            description: issueDescription,
            s3_object_key: filename
        }
        let result = await addIssueAPI(data, token);
        // Based on result fire the event
    }

    
</script>


<section class="container mt-4">
    <div class="row">
        <div class="col-12 d-flex justify-content-between align-items-center mb-3">
            <h2 class="mb-0">Issues</h2>
            <button on:click={addIssueDIV}> + Add Issue </button>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-body">
                    {#if issues.length === 0}
                        <p class="text-center text-muted py-5">No issue is there</p>
                    {:else}
                        <!-- Listing All Issues -->
                    {/if}
                </div>
            </div>
        </div>
    </div>
</section>

{#if showAddIssuediv}
    <div class="add-issue-popup" class:show={showAddIssuediv}>
        <div class="popup-content">
        <div class="popup-header">
            <h3>Add New Issue</h3>
            <button type="button" class="close-btn" on:click={() => showAddIssuediv = false}>&times;</button>
        </div>
        <div class="popup-body">
            <div class="form-group mb-3">
            <label for="issueTitle">Title</label>
            <input type="text" class="form-control" id="issueTitle" bind:value={issueTitle} placeholder="Enter issue title">
            </div>
            <div class="form-group mb-3">
            <label for="issueDescription">Description</label>
            <textarea class="form-control" id="issueDescription" bind:value={issueDescription} rows="4" placeholder="Describe the issue"></textarea>
            </div>
            <div class="form-group mb-4">
            <label for="issueFile">Attachment (Optional)</label>
            <input type="file" class="form-control"  id="issueFile" filename={filename} on:change={addAttachment} name="attachment">
            </div>
        </div>
        <div class="popup-footer">
            <button type="button" class="btn btn-secondary" on:click={() => showAddIssuediv = false}>Cancel</button>
            <button type="button" class="btn btn-secondary" on:click={addIssue}>Add Issue</button>
        </div>
        </div>
    </div>
{/if}

<style>
    @import '$lib/styles/dashboard.css';
</style>