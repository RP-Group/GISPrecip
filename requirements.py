import sys, os

# Path where the virtual environment (venv) was created
venv_dir = os.path.expanduser("~/GISPrecip")

# Path to the site-packages directory (where installed packages reside)
site_packages = os.path.join(venv_dir, "lib", "python3.12", "site-packages")

# Append the site-packages path to the system path to make installed packages available to the script
sys.path.append(site_packages)

print("Packages installed added.")
