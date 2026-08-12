# Generator strony: czyta treść z Postgresa i składa statyczne www/.
# Python 3.12 — ta sama wersja, którą budowano dotychczas (__pycache__/*.cpython-312).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONDONTWRITEBYTECODE=1

# lxml wymaga bibliotek systemowych (używa go _validate.py i localize_site.py).
# git + openssh-client — do hostowanej publikacji (PANEL_DEPLOY=git robi push
# do repo, patrz admin_api._publish_git). Lokalnie nieużywane, ale lekkie.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libxml2 libxslt1.1 git openssh-client \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /site

# Domyślnie: eksport treści z bazy + pełny build
CMD ["python", "/builder/build_all.py"]
