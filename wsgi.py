from app import app, config

if __name__ == "__main__":
    app.run(host=config.get("HOST"), port=config.get("PORT"), debug=config.get("DEBUG"))
