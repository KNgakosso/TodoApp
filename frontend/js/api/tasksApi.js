export async function getTasks() {
    try {
        const res = await fetch("http://127.0.0.1:8000/tasks")
        return await res.json();
    } catch(err) {
        console.log(err);
    }
}

export async function getOngoingTasks() {
    try {
        const res = await fetch("http://127.0.0.1:8000/tasks/status/ongoing")
        return await res.json();
    } catch(err) {
        console.log(err);
    }
}


export async function getCompletedTasks() {
    try {
        const res = await fetch("http://127.0.0.1:8000/tasks/status/completed")
        return await res.json();
    } catch(err) {
        console.log(err);
    }
}

export async function getTask(id) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/tasks/${id}`)
        return await res.json();
    } catch(err) {
        console.log(err);
    }
}
export async function createTask(listName, data) {
    const params = listName ? `?list_name=${encodeURIComponent(listName)}` : "";
    try {
        const res = await fetch(`http://127.0.0.1:8000/tasks${params}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        return await res.json();
    } catch (err) {
        console.log(err);
    }
}

export async function updateTask(id, data) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/tasks/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        return await res.json();
    } catch (err) {
        console.log(err);
    }
}

export async function toggleTask(id) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/tasks/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            }
    });
        return await res.json();
    } catch (err) {
        console.log(err);
    }
}

export async function deleteTask(id) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/tasks/${id}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json();
    } catch (err) {
        console.log(err);
    }
}