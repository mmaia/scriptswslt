package br.com.maweb.estudos.webapp.action;

import java.util.List;

import br.com.maweb.estudos.model.Person;
import br.com.maweb.estudos.service.PersonManager;

import com.opensymphony.xwork2.Preparable;

public class AjaxTestAction extends BaseAction implements Preparable {
    private static final long serialVersionUID = 378605805550104346L;

    private PersonManager personManager;
    
    private List<Person>        persons;

    private Long              id;

    @Override
    public String execute() throws Exception {
        log.debug("just getting the stuf");
        persons = (List<Person>) getRequest().getAttribute("persons");
        if (persons == null) {
            log.debug("just ones please");
            persons = personManager.getAll();
            getRequest().setAttribute("persons", persons);
        } else {
            log.debug("persons" + persons.size());
        }
        return SUCCESS;
    }

    public List<Person> getPersons() {
        return persons;
    }

    public void setPersons(List<Person> persons) {
        this.persons = persons;
    }

    public String remove() throws Exception {
        log.debug("do some removing here when i feel like it id:" + id);
        if (persons != null) {
            log.debug("before persons" + persons.size());
            persons.remove((id.intValue() - 1));
            log.debug("after persons" + persons.size());
        }
        return SUCCESS;
    }

    public String save() throws Exception {
        log.debug("do some saving here when i feel like it");
        return execute();
    }

    public String ajax() {
        log.debug("ajax is doing something id:"+id);
        return "ajax";
    }

    public String edit() throws Exception {
        log.debug("do some editing here when i feel like it");
        return execute();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void prepare() throws Exception {
        log.debug("i'm getting prepared!!!");

    }

	public void setPersonManager(PersonManager personManager) {
		this.personManager = personManager;
	}
}