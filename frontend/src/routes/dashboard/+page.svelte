<script>
    import {addAttachmentAPI, addIssueAPI, getAllIssuesAPI, updateIssueAPI, deleteIssueAPI} from '$lib/issues/issueManagement';
    import {useClerkContext} from 'svelte-clerk/client';
    import {role} from '$lib/issues/roles';

    import Swal from 'sweetalert2';

    let issues = [];
    let showAddIssuediv = false;
    let showEditIssuediv = false;
    let filename = null;

    let issueTitle = '';
    let issueDescription = '';


    let editingIssue = null;
    let editIssueTitle = '';
    let editIssueDescription = '';
    let editIssueStatus = '';
    let editIssueSeverity = '';
    let editIssueId = null;

    const statusOptions = ['open', 'triaged', 'in_progress', 'done'];
    const severityOptions = ['low', 'medium', 'high'];

    function addIssueDIV(){
        showAddIssuediv = true;
    }

    function openEditModal(issue) {
        editingIssue = issue;
        editIssueTitle = issue.title;
        editIssueDescription = issue.description;
        editIssueStatus = issue.status;
        editIssueSeverity = issue.severity || 'low'; 
        editIssueId = issue.issue_id;
        showEditIssuediv = true;
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

    }


    let getAllIssues = async () => {
        const token = await get_token();
        let issuesData = await getAllIssuesAPI(token);

        if (issuesData != 500)
            issues = issuesData;

    }

    let updateIssue = async() => {
        const token = await get_token();
        
        let data = {
            issue_id: editIssueId,
            title: editIssueTitle,
            description: editIssueDescription,
            status: editIssueStatus,
            severity: editIssueSeverity
        }
        
        try {
            console.log("Issue ID: ",data['issue_id'])
            let result = await updateIssueAPI(data, token);
            if (result !== 500) {
                await getAllIssues();
                showEditIssuediv = false;
                console.log("Issue updated successfully:", result);
            }
        } catch (error) {
            console.error("Error updating issue:", error);
        }
    }

    let confirmDelete = async(issueId) => {
        const result = await Swal.fire({
            theme: 'dark',
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Yes, delete it!'
        });
        
        if (result.isConfirmed) {
            let result = await deleteIssue(issueId);

            const s_result = await Swal.fire({                
                theme: 'dark',
                title: 'Deleted!',
                text: result ? 'Your issue has been deleted.' : 'Error in deleting the issue.',
                icon: result ? 'success' : 'error'
            });

            if (s_result.isConfirmed){
            await fetchData();
        }
        }

    }

    let deleteIssue = async(issueId) => {
        const token = await get_token();
        let data = await deleteIssueAPI(issueId,token);

        if(data == 200)
            return true;

        return false;
    }
    const fetchData = async() => {
        await getAllIssues();
    };

    
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
                        
                    <div class="issues-container">
                        {#each issues as issue}
                            <div class="issue-card mb-3">
                                <div class="issue-header d-flex justify-content-between">
                                    <h5 class="issue-title">{issue.title}</h5>
                                    <div>
                                        <span class="badge bg-{issue.status === 'open' ? 'warning' : 'success'} me-1">{issue.status}</span>
                                        <span class="badge bg-{
                                            issue.severity === 'low' ? 'info' : 
                                            issue.severity === 'medium' ? 'warning' : 'danger'
                                        } me-1">{issue.severity || 'low'}</span>
                                        <button class="btn btn-sm btn-outline-primary ms-2" on:click={() => openEditModal(issue)}>Edit</button>
                                        <button class="btn btn-sm btn-outline-danger ms-1" on:click={() => confirmDelete(issue.issue_id)}>
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="issue-body">
                                    <p class="issue-description">{issue.description}</p>
                                    {#if issue.s3_object_key}
                                        <div class="issue-attachment">
                                            <small class="text-muted">Attachment: {issue.s3_object_key}</small>
                                        </div>
                                    {/if}
                                </div>
                                <div class="issue-footer d-flex justify-content-between text-muted">
                                    <small>Created: {new Date(issue.created_at).toLocaleDateString()}</small>
                                    <small>Updated: {new Date(issue.updated_at).toLocaleDateString()}</small>
                                </div>
                            </div>
                        {/each}
                    </div>
                        <!-- Listing All Issues End-->
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

{#if showEditIssuediv && editingIssue}<div class="add-issue-popup" class:show={showEditIssuediv}>
    <div class="popup-content">
        <div class="popup-header">
            <h3>Edit Issue</h3>
            <button type="button" class="close-btn" on:click={() => showEditIssuediv = false}>&times;</button>
        </div>
        <div class="popup-body">
            <div class="form-group mb-3">
                <label for="editIssueTitle">Title</label>
                <input type="text" class="form-control" id="editIssueTitle" bind:value={editIssueTitle} placeholder="Enter issue title">
            </div>
            <div class="form-group mb-3">
                <label for="editIssueDescription">Description</label>
                <textarea class="form-control" id="editIssueDescription" bind:value={editIssueDescription} rows="4" placeholder="Describe the issue"></textarea>
            </div>
            <div class="form-group mb-3">
                <label for="editIssueStatus">Status</label>
                <select class="form-select" id="editIssueStatus" bind:value={editIssueStatus}>
                    {#each statusOptions as status}
                        <option value={status}>{status.replace('_', ' ')}</option>
                    {/each}
                </select>
            </div>
            <div class="form-group mb-3">
                <label for="editIssueSeverity">Severity</label>
                <select class="form-select" id="editIssueSeverity" bind:value={editIssueSeverity}>
                    {#each severityOptions as severity}
                        <option value={severity}>{severity}</option>
                    {/each}
                </select>
            </div>
        </div>
        <div class="popup-footer">
            <button type="button" class="btn btn-secondary" on:click={() => showEditIssuediv = false}>Cancel</button>
            <button type="button" class="btn btn-primary" on:click={updateIssue}>Update Issue</button>
        </div>
    </div>
</div>
{/if}

<div style="display:none;">{fetchData()}</div>

<style>
    @import '$lib/styles/dashboard.css';
    
    
</style>