# 1. Pull an official, enterprise-hardened minimal Python 3.11 base layer
FROM python:3.11-slim

# 2. Establish an isolated internal workspace container directory
WORKDIR /app

# 3. Port over the dependency manifest definition lists ahead of resource code
COPY requirements.txt .

# 4. Compile and install platform packages with caching optimizations disabled
RUN pip install --no-cache-dir -r requirements.txt

# 5. Populate the workspace folder with internal scanner and mitigation python modules
COPY . .

# 6. Bind proxy routing listeners securely onto internal networking Port 8000
EXPOSE 8000

# 7. Initialize the runtime framework as a background daemon process listener
CMD ["uvicorn", "iris_engine:app", "--host", "0.0.0.0", "--port", "8000"]
