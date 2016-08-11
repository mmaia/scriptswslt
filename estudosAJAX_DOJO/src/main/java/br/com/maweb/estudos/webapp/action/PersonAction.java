package br.com.maweb.estudos.webapp.action;

import com.opensymphony.xwork2.Preparable;
import br.com.maweb.estudos.service.PersonManager;
import br.com.maweb.estudos.model.Person;
import br.com.maweb.estudos.webapp.action.BaseAction;

import java.util.List;

public class PersonAction extends BaseAction implements Preparable {
    private PersonManager personManager;
    private List persons;
    private Person person;
    private Long  id;

    public void setPersonManager(PersonManager personManager) {
        this.personManager = personManager;
    }

    public List getPersons() {
        return persons;
    }

    /**
     * Grab the entity from the database before populating with request parameters
     */
    public void prepare() {
        if (getRequest().getMethod().equalsIgnoreCase("post")) {
            // prevent failures on new
            String personId = getRequest().getParameter("person.id");
            if (personId != null && !personId.equals("")) {
                person = personManager.get(new Long(personId));
            }
        }
    }

    public String list() {
        persons = personManager.getAll();
        return SUCCESS;
    }

    public void setId(Long  id) {
        this. id =  id;
    }

    public Person getPerson() {
        return person;
    }

    public void setPerson(Person person) {
        this.person = person;
    }

    public String delete() {
        personManager.remove(person.getId());
        saveMessage(getText("person.deleted"));

        return SUCCESS;
    }

    public String edit() {
        if (id != null) {
            person = personManager.get(id);
        } else {
            person = new Person();
        }

        return SUCCESS;
    }

    public String save() throws Exception {
        if (cancel != null) {
            return "cancel";
        }

        if (delete != null) {
            return delete();
        }

        boolean isNew = (person.getId() == null);

        personManager.save(person);

        String key = (isNew) ? "person.added" : "person.updated";
        saveMessage(getText(key));

        if (!isNew) {
            return INPUT;
        } else {
            return SUCCESS;
        }
    }
}