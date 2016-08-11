package br.com.maweb.estudos.service;

import br.com.maweb.estudos.service.GenericManager;
import br.com.maweb.estudos.model.Person;

import java.util.List;
import javax.jws.WebService;

@WebService
public interface PersonManager extends GenericManager<Person, Long> {
    
}