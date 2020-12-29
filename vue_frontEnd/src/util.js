const instance = axios.create({
	baseURL: 'http://127.0.0.1:5000/',
	timeout: 3000,
	header: {
	'Content-Type': 'application/x-www-form-urlencoded'
	}
}) 

export default instance