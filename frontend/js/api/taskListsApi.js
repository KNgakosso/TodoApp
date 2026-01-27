export async function getTaskLists() {
    try {
        const res = await fetch("http://127.0.0.1:8000/lists")
        return await res.json();
    } catch(err) {
        console.log(err);
    }
}

export async function getTaskList(name) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/lists/${name}`)
        return await res.json();
    } catch(err) {
        console.log(err);
    }
}
export async function createTaskList(data) {
    try {
        const res = await fetch("http://127.0.0.1:8000/lists", {
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

export async function deleteTaskList(name) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/lists/${name}`, {
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

export async function createTaskFromTaskList(name, data) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/lists/${name}/task`, {
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