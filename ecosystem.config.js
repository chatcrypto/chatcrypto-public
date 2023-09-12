module.exports = {
    apps: [
        {
            name: "chatcryptor-backend-api",
	    cwd: '/home/apscan/projects/chatcryptor/langchainloaders',
            script: "./main.py",
            error_file: '/data/npm_logs/chatcryptor-backend-api-error.log',
            out_file: '/data/npm_logs/chatcryptor-backend-api.log',
	    interpreter: '/home/apscan/projects/chatcryptor/venv/bin/python'
        }
    ]   
}
