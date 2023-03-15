//package yongyong.graduate.service;
//
//import lombok.RequiredArgsConstructor;
//import org.springframework.data.domain.Page;
//import org.springframework.data.domain.Pageable;
//import org.springframework.stereotype.Service;
//import yongyong.graduate.domain.Doc;
//import yongyong.graduate.domain.DocRepository;
//
//@Service
//@RequiredArgsConstructor
//public class DocService {
//
//    private final DocRepository docRepository;
//
//    public Page<Doc> findAllPage(int startAt) {
//        Pageable pageable = PageRequest.of(startAt, 2);
//        return docRepository.findAll(pageable);
//    }
//
//    // 페이지 처리를 위한 메소드
//    public Page<Doc> docList(Pageable pageable) {
//        return docRepository.findAll(pageable);
//    }
//}