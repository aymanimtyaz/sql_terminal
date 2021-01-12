# sql-terminal - Command line querying utility for PostgreSQL
A command line utility in less than - 250 lines of code. Connect to and query remote as well as private (SSH tunnel accessible) PostgreSQL databases right from your terminal!
WRITTEN IN PYTHON

## Installation
1. Make sure you have Python 3 installed and working.
2. Clone the repo and cd into it:
```
git clone https://github.com/aymanimtyaz/sql_terminal.git
```
3. Install prerequisites using pip, preferably in a new environment:
```
pip install -r requirements.txt
```
## Usage
### Basic usage
To run the utility, cd into the repo and run sql_terminal.py:
```
python3 sql_terminal.py
```
Enter the credentials needed to connect to your database when prompted by the program.
When done with the program, hit **Ctrl + C to exit**.
### Passing credentials as command line arguments
You can store your credentials in a .json file and pass the filename (if it is in the directory/repo) or the filepath as an argument to connect to your database:
```
python3 sql_terminal.py credentials.json
```
The credentials file should be a json file formatted as such:
```
{
	"host":"hostname or ip address of the database server",
	"port":"port on which we can connect to the database",
	"database":"name of the database to connect to,
	"username":"postgres username to connect as,
	"password":"postgres password",
	"autocommit":"y",
	"ssh_host":"If accessing the database through an SSH tunnel, enter the ip/hostname of the SSH gateway here",
	"ssh_port":"port through which we can SSH to the SSH gateway, default 22",
	"ssh_username":"username to SSH as",
	"ssh_password":"password for SSH if needed, if not, let this be empty",
	"ssh_pkey":"filepath to an SSH pKey if needed, let this be empty if not needed"
}
```
If using a credentials file, the **first 6 fields are necessary in all cases**. Add the SSH fields only if needed.
The program will ask you if you would like to connect through an SSH tunnel every single time, regardless of whether the SSH credentials were added in the credentials file.
The name of the credentials file doesn't have to be *credentials*, however it must be a .json file formatted as shown above.
If not using a field in the credentials, like ssh_password for example, leave it blank as:
```
"ssh_password":""
```
### Passing SQL through the command line
If you have a ***.txt*** or ***.sql*** file that has some SQL in it. You can execute them by passing their filename(if in the directory/repo) or the filepath as:
```
python3 sql_terminal.py some_sql.sql
```
You can pass both a credentials file and an SQL file as command line arguments in any order. For example:
```
python3 sql_terminal.py creds.json sql.sql
```
is valid, and so is:
```
python3 sql_terminal.py sql.sql creds.json
```
**NOTE**: If executing SQL through a file, **make sure that autocommit is set to 'y'** in the credentials file, or if not using a credentials file, answer 'y' when "run with autocommit? (y/n)" is asked.
### A note on autocommit
The **autocommit option should preferably be set to 'y'**. If set to 'n'. Queries made to the database will only persist if the COMMIT command is sent after. However, the behaviour is buggy and some commands will autocommit even if the autocommit option is set to 'n'. This will be fixed in an update soon.

#### This is a work in progress and bugs may be aplenty. If you have any questions, feel free to email me at aymanimtyaz@gmail.com :)
